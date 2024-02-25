package main

import (
	"context"
	"encoding/json"
	"io"
	"log"
	"net/http"
	"os"

	uuid "github.com/google/uuid"

	scryfall "github.com/BlueMonday/go-scryfall"
	"github.com/gin-gonic/gin"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func main() {
	ctx := context.Background()
	client, err := scryfall.NewClient()
	if err != nil {
		log.Fatal(err)
	}
	mongourl := os.Getenv("mongo")
	mongoclient, err := mongo.Connect(ctx, options.Client().ApplyURI(mongourl))
	if err != nil {
		log.Fatal(err)
	}
	defer func() {
		if err := mongoclient.Disconnect(context.TODO()); err != nil {
			panic(err)
		}
	}()
	router := gin.Default()
	v1 := router.Group("/api/v1")
	v1.GET("/update", updateBulk(context.TODO(), client, mongoclient))
	v1.POST("/update/custom", postCustom(mongoclient))
	router.Run("localhost:8080")
}

func postCustom(mng *mongo.Client) gin.HandlerFunc {
	return func(c *gin.Context) {
		var stuff []FlamewaveTTSCard
		bdydec := json.NewDecoder(c.Request.Body)
		err := bdydec.Decode(&stuff)
		if err != nil {
			c.JSON(http.StatusBadRequest, nil)
			return
		}
		// Ensure that set codes don't conflict.
		coll := mng.Database("flamewave").Collection("cards")
		var submissions []mongo.WriteModel = make([]mongo.WriteModel, len(stuff))
		for i, m := range stuff {
			if len(m.FlamewaveID) == 0 {
				stuff[i].FlamewaveID = uuid.New().String()
			}
			if contains(SetCodes, m.SetCode) {
				c.JSON(http.StatusBadRequest, "One or more submitted cards use an illegal set code.")
				return
			} else {
				submissions[i] = mongo.NewReplaceOneModel().SetFilter(bson.D{{Key: "flamewave_id", Value: m.FlamewaveID}}).SetReplacement(m).SetUpsert(true)
			}
		}
		coll.BulkWrite(context.TODO(), submissions)
	}
}

type IntermediateCardStruct struct {
	Card     *FlamewaveTTSCard
	Priority bool
}

func updateBulk(cx context.Context, ct *scryfall.Client, mg *mongo.Client) gin.HandlerFunc {
	return func(c *gin.Context) {
		bulkList, err := ct.ListBulkData(cx)
		if err != nil {
			log.Fatal(err)
		}
		for _, entry := range bulkList {
			if entry.Type == "default_cards" {
				resp, err := http.Get(entry.DownloadURI)
				if err != nil {
					log.Fatal(err)
				}
				defer resp.Body.Close()
				coll := mg.Database("flamewave").Collection("cards")
				var counter uint32 = 0
				var submissions = []mongo.WriteModel{}
				dec := json.NewDecoder(resp.Body)
				dec.Token()
				for dec.More() {
					var m scryfall.Card
					if err := dec.Decode(&m); err == io.EOF {
						break
					} else if err != nil {
						log.Fatal(err)
					}
					counter++
					crd := NewFlamewaveTTSCard(m, counter)
					submissions = append(submissions, mongo.NewReplaceOneModel().SetFilter(bson.D{{Key: "flamewave_id", Value: m.ID}}).SetReplacement(crd).SetUpsert(true))
				}
				dec.Token()
				coll.BulkWrite(context.TODO(), submissions)
			}
		}
	}
}
