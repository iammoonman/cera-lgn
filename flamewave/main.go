package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"

	uuid "github.com/google/uuid"
	tabletopsimulator "github.com/iammoonman/go-tabletop-simulator"

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
	v1.GET("/scryfall_id/:id", getSingle(context.TODO(), mongoclient, "scryfall_id"))
	v1.GET("/flamewave_id/:id", getSingle(context.TODO(), mongoclient, "flamewave_id"))
	v1.GET("/oracle_id/:id", getSingle(context.TODO(), mongoclient, "oracle_id"))
	v1.GET("/set/:id", getSet(context.TODO(), mongoclient))
	v1.GET("/sets", getSets())
	v1.POST("/collection", getCollection(context.TODO(), mongoclient))
	router.Static("/index", "./static")
	router.Run(":8080")
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
		coll := mg.Database("flamewave").Collection("cards")
		coll.DeleteMany(context.TODO(), bson.D{{Key: "oracle_id", Value: bson.D{{Key: "$gte", Value: " "}}}})
		var submissions = []mongo.WriteModel{}
		for _, entry := range bulkList {
			if entry.Type == "default_cards" {
				resp, err := http.Get(entry.DownloadURI)
				if err != nil {
					log.Fatal(err)
				}
				defer resp.Body.Close()
				var counter uint32 = 0
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
					// submissions = append(submissions, mongo.NewReplaceOneModel().SetFilter(bson.D{{Key: "flamewave_id", Value: m.ID}}).SetReplacement(crd).SetUpsert(true))
					submissions = append(submissions, mongo.NewInsertOneModel().SetDocument(crd))
				}
				dec.Token()
			}
		}
		var f = false
		var t = true
		var n = 0
		coll.BulkWrite(context.TODO(), submissions[n:n+10000], &options.BulkWriteOptions{Ordered: &f, BypassDocumentValidation: &t})
		n = n + 10000
		coll.BulkWrite(context.TODO(), submissions[n:n+10000], &options.BulkWriteOptions{Ordered: &f, BypassDocumentValidation: &t})
		n = n + 10000
		coll.BulkWrite(context.TODO(), submissions[n:n+10000], &options.BulkWriteOptions{Ordered: &f, BypassDocumentValidation: &t})
		n = n + 10000
		coll.BulkWrite(context.TODO(), submissions[n:n+10000], &options.BulkWriteOptions{Ordered: &f, BypassDocumentValidation: &t})
		n = n + 10000
		coll.BulkWrite(context.TODO(), submissions[n:n+10000], &options.BulkWriteOptions{Ordered: &f, BypassDocumentValidation: &t})
		n = n + 10000
		coll.BulkWrite(context.TODO(), submissions[n:n+10000], &options.BulkWriteOptions{Ordered: &f, BypassDocumentValidation: &t})
		n = n + 10000
		coll.BulkWrite(context.TODO(), submissions[n:n+10000], &options.BulkWriteOptions{Ordered: &f, BypassDocumentValidation: &t})
		n = n + 10000
		coll.BulkWrite(context.TODO(), submissions[n:n+10000], &options.BulkWriteOptions{Ordered: &f, BypassDocumentValidation: &t})
		n = n + 10000
		coll.BulkWrite(context.TODO(), submissions[n:], &options.BulkWriteOptions{Ordered: &f, BypassDocumentValidation: &t})
	}
}

func getSingle(cx context.Context, mg *mongo.Client, id string) gin.HandlerFunc {
	return func(c *gin.Context) {
		y := c.Param(id)
		coll := mg.Database("flamewave").Collection("cards")
		x := coll.FindOne(cx, bson.D{{Key: id, Value: y}})
		var l FlamewaveTTSCard
		x.Decode(l)
		var card = tabletopsimulator.NewSingleCardObject(l.ContainedObjectsEntry.Nickname, l.ContainedObjectsEntry.Description, l.ContainedObjectsEntry.Memo, l.CustomDeckEntry)
		card.States = l.ContainedObjectsEntry.States
		card.LuaScript = l.ContainedObjectsEntry.LuaScript
		c.JSON(200, &card)
	}
}

func getSet(cx context.Context, mg *mongo.Client) gin.HandlerFunc {
	return func(c *gin.Context) {
		y := c.Param("id")
		coll := mg.Database("flamewave").Collection("cards")
		x, e := coll.Find(cx, bson.D{{Key: "set", Value: y}})
		if e != nil {
			return
		}
		var l []FlamewaveTTSCard
		x.All(cx, &l)
		var deck = tabletopsimulator.NewDeckObject()
		for q := 0; q < len(l); q++ {
			var c = l[q]
			deck.ContainedObjects = append(deck.ContainedObjects, c.ContainedObjectsEntry)
			deck.DeckIDs = append(deck.DeckIDs, int((q+1)*100))
			deck.CustomDeck[fmt.Sprintf("%d", q+1)] = c.CustomDeckEntry
		}
		c.JSON(200, &deck)
	}
}

func getCollection(cx context.Context, mg *mongo.Client) gin.HandlerFunc {
	return func(c *gin.Context) {
		var t []FlamewaveIdentifier
		c.BindJSON(&t)
		if len(t) == 0 || len(t) > 1000 {
			return
		}
		coll := mg.Database("flamewave").Collection("cards")
		var l []FlamewaveTTSCard
		lstRequests := make(bson.D, len(t))
		for i, thing := range t {
			if thing.FlamewaveId != "" {
				lstRequests[i] = bson.E{Key: "$and", Value: bson.D{
					{Key: "flamewave_id", Value: thing.FlamewaveId},
				}}
			} else if thing.ScryfallId != "" {
				lstRequests[i] = bson.E{Key: "$and", Value: bson.D{
					{Key: "scryfall_id", Value: thing.ScryfallId},
				}}
			} else if thing.CollectorNumber != "" && thing.SetCode != "" {
				lstRequests[i] = bson.E{Key: "$and", Value: bson.D{
					{Key: "cn", Value: thing.CollectorNumber},
					{Key: "set", Value: thing.SetCode},
				}}
			} else if thing.OracleId != "" {
				lstRequests[i] = bson.E{Key: "$and", Value: bson.D{
					{Key: "oracle_id", Value: thing.OracleId},
				}}
			} else {
				return
			}
		}
		filter := bson.D{{Key: "$or", Value: lstRequests}}
		x, err := coll.Find(cx, filter, options.Find().SetProjection(bson.D{{Key: "CustomDeckEntry", Value: 0}, {Key: "ContainedObjectsEntry", Value: 0}}))
		if err != nil {
			log.Fatal(err)
		}
		x.All(context.TODO(), &l)
		outputMap := make(map[string]IntermediateCardStruct)
		var deck = tabletopsimulator.NewDeckObject()
		for _, c := range l {
			for x, identity := range t {
				if len(identity.OracleId) > 0 && identity.OracleId == c.OracleID {
					if o, err := outputMap[c.OracleID]; !err {
						if !o.Priority {
							outputMap[c.OracleID] = IntermediateCardStruct{Card: &c, Priority: false}
						}
					}
				}
				if (identity.CollectorNumber == c.CollectorNumber && identity.SetCode == c.SetCode) || identity.ScryfallId == c.ScryfallID {
					outputMap[c.OracleID] = IntermediateCardStruct{Card: &c, Priority: true}
					t[x].OracleId = c.OracleID
				}
			}
		}
		for n, i := range t {
			for q := 0; q <

				int(i.Quantity); q++ {
				var c = outputMap[i.OracleId]
				deck.ContainedObjects = append(deck.ContainedObjects, c.Card.ContainedObjectsEntry)
				deck.DeckIDs = append(deck.DeckIDs, int(n*100))
				deck.CustomDeck[fmt.Sprintf("%d", n)] = c.Card.CustomDeckEntry
			}
		}
		c.JSON(http.StatusOK, &deck)
	}
}

func getSets() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.JSON(http.StatusOK, SetCodes)
	}
}
