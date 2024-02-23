package main

import (
	"context"
	"encoding/json"
	tabletopsimulator "flamewave/tabletopsimulator"
	"fmt"
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
	// router.GET("/", postCollection)
	// router.GET("/playground", getStuff) // There's also a JSON representation for stuff here.
	// router.GET("/simulator", getStuff)  // Returns full JSON string for spawning an object. Pass directly into spawnObjectData.
	v1.POST("/simulator/collection", postCollection(context.TODO(), client, mongoclient))
	v1.GET("/update", updateBulk(context.TODO(), client, mongoclient))
	v1.POST("/update/custom", postCustom(mongoclient))
	v1.GET("/simulator/oracle/:oracle_id", getSingleOracle(context.TODO(), mongoclient))
	v1.GET("/simulator/scryfall/:scryfall_id", getSingleScryfall(context.TODO(), mongoclient))
	v1.GET("/simulator/flamewave/:flamewave_id", getSingleFlamewave(context.TODO(), mongoclient))
	router.Run("localhost:8080")
}

func getSingleFlamewave(cx context.Context, mg *mongo.Client) gin.HandlerFunc {
	return func(c *gin.Context) {
		flamewave_id := c.Param("flamewave_id")
		if len(flamewave_id) == 0 {
			return
		}
		coll := mg.Database("flamewave").Collection("cards")
		x := coll.FindOne(cx, bson.E{Key: "flamewave_id", Value: flamewave_id})
		var l FlamewaveTTSCard
		x.Decode(l)
		var deck = tabletopsimulator.NewDeckObject()
		deck.ContainedObjects = append(deck.ContainedObjects, l.ContainedObjectsEntry)
		deck.CustomDeck[fmt.Sprintf("%d", 1)] = l.CustomDeckEntry
		deck.DeckIDs = append(deck.DeckIDs, 1)
		c.JSON(http.StatusOK, deck)
	}
}

func getSingleScryfall(cx context.Context, mg *mongo.Client) gin.HandlerFunc {
	return func(c *gin.Context) {
		scryfall_id := c.Param("scryfall_id")
		if len(scryfall_id) == 0 {
			return
		}
		coll := mg.Database("flamewave").Collection("cards")
		x := coll.FindOne(cx, bson.E{Key: "scryfall_id", Value: scryfall_id})
		var l FlamewaveTTSCard
		x.Decode(l)
		var deck = tabletopsimulator.NewDeckObject()
		deck.ContainedObjects = append(deck.ContainedObjects, l.ContainedObjectsEntry)
		deck.CustomDeck[fmt.Sprintf("%d", 1)] = l.CustomDeckEntry
		deck.DeckIDs = append(deck.DeckIDs, 1)
		c.JSON(http.StatusOK, deck)
	}
}

func getSingleOracle(cx context.Context, mg *mongo.Client) gin.HandlerFunc {
	return func(c *gin.Context) {
		oracle_id := c.Param("oracle_id")
		if len(oracle_id) == 0 {
			return
		}
		coll := mg.Database("flamewave").Collection("cards")
		x := coll.FindOne(cx, bson.E{Key: "oracle_id", Value: oracle_id})
		var l FlamewaveTTSCard
		x.Decode(l)
		var deck = tabletopsimulator.NewDeckObject()
		deck.ContainedObjects = append(deck.ContainedObjects, l.ContainedObjectsEntry)
		deck.CustomDeck[fmt.Sprintf("%d", 1)] = l.CustomDeckEntry
		deck.DeckIDs = append(deck.DeckIDs, 1)
		c.JSON(http.StatusOK, deck)
	}
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

func postCollection(cx context.Context, ct *scryfall.Client, mg *mongo.Client) gin.HandlerFunc {
	return func(c *gin.Context) {
		// var stuff []Identifier
		// stuff = append(stuff, Identifier{ScryfallId: "4d3f41dc-72f6-4346-b95f-4813addb5af0"})
		// stuff = append(stuff, Identifier{CollectorNumber: "1", SetCode: "lea", Quantity: 4})
		// stuff = append(stuff, Identifier{OracleId: "ca00eb17-e5c3-42c8-a665-431f5f95b67f"})
		bdydec := json.NewDecoder(c.Request.Body)
		var stuff []FlamewaveIdentifier
		err := bdydec.Decode(&stuff)
		if err != nil {
			c.JSON(http.StatusBadRequest, nil)
			return
		}
		if len(stuff) == 0 || len(stuff) > 1000 {
			c.JSON(http.StatusBadRequest, nil)
			return
		}
		coll := mg.Database("flamewave").Collection("cards")
		var l []FlamewaveTTSCard
		// If flamewave_id in the list of flamewave ids from the identifiers
		// If scryfall_id in the list of scryfall ids...
		// etc
		lstRequests := make(bson.D, len(stuff))
		for i, thing := range stuff {
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
		x, err := coll.Find(cx, filter)
		if err != nil {
			log.Fatal(err)
		}
		x.All(context.TODO(), l)
		outputMap := make(map[string]IntermediateCardStruct)
		var deck = tabletopsimulator.NewDeckObject()
		for _, c := range l {
			for x, identity := range stuff {
				if len(identity.OracleId) > 0 && identity.OracleId == c.OracleID {
					if o, err := outputMap[c.OracleID]; !err {
						if !o.Priority {
							outputMap[c.OracleID] = IntermediateCardStruct{Card: &c, Priority: false}
						}
					}
				}
				if (identity.CollectorNumber == c.CollectorNumber && identity.SetCode == c.SetCode) || identity.ScryfallId == c.ScryfallID {
					outputMap[c.OracleID] = IntermediateCardStruct{Card: &c, Priority: true}
					stuff[x].OracleId = c.OracleID
				}
			}
		}
		for n, i := range stuff {
			for q := 0; q <= int(i.Quantity); q++ {
				var c = outputMap[i.OracleId]
				deck.ContainedObjects = append(deck.ContainedObjects, c.Card.ContainedObjectsEntry)
				deck.DeckIDs = append(deck.DeckIDs, int(n*100))
				deck.CustomDeck[fmt.Sprintf("%d", n)] = c.Card.CustomDeckEntry
			}
		}
		// outputSave := TTSSave{ObjectStates: []TTSDeckObject{deck}}
		c.JSON(http.StatusOK, deck)
	}
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
