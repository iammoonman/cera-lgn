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
	v1.GET("/site/set/:id", getSetWebsite(context.TODO(), mongoclient))
	v1.GET("/sets", getSets(context.TODO(), mongoclient))
	v1.GET("/cube/:id", getCubeCobra(context.TODO(), mongoclient))
	v1.POST("/collection", getCollection(context.TODO(), mongoclient))
	router.StaticFile("/", "./static/index.html")
	router.StaticFile("/set.html", "./static/set.html")
	router.Run(":8080")
}

func postCustom(mng *mongo.Client) gin.HandlerFunc {
	return func(c *gin.Context) {
		var stuff []FlamewaveTTSCard
		user, pass, ok := c.Request.BasicAuth()
		if !ok || user != os.Getenv("user") || pass != os.Getenv("pass") {
			c.Status(http.StatusUnauthorized)
			return
		}
		bdydec := json.NewDecoder(c.Request.Body)
		err := bdydec.Decode(&stuff)
		if err != nil {
			c.JSON(http.StatusBadRequest, nil)
			return
		}
		// Ensure that set codes don't conflict.
		coll := mng.Database("Flamewave").Collection("cards")
		var submissions []mongo.WriteModel = make([]mongo.WriteModel, len(stuff))
		for i, m := range stuff {
			if len(m.FlamewaveID) == 0 {
				stuff[i].FlamewaveID = uuid.New().String()
			}
			submissions[i] = mongo.NewReplaceOneModel().SetFilter(bson.D{{Key: "flamewave_id", Value: m.FlamewaveID}}).SetReplacement(m).SetUpsert(true)
		}
		coll.BulkWrite(context.TODO(), submissions)
	}
}

type IntermediateCardStruct struct {
	Card     FlamewaveTTSCard
	Priority bool
}

func updateBulk(cx context.Context, ct *scryfall.Client, mg *mongo.Client) gin.HandlerFunc {
	return func(c *gin.Context) {
		user, pass, ok := c.Request.BasicAuth()
		if !ok || user != os.Getenv("user") || pass != os.Getenv("pass") {
			c.Status(http.StatusUnauthorized)
			return
		}
		bulkList, err := ct.ListBulkData(cx)
		if err != nil {
			log.Fatal(err)
		}
		coll := mg.Database("Flamewave").Collection("cards")
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
		coll.BulkWrite(context.TODO(), submissions, &options.BulkWriteOptions{Ordered: &f, BypassDocumentValidation: &t})
	}
}

func getSingle(cx context.Context, mg *mongo.Client, id string) gin.HandlerFunc {
	return func(c *gin.Context) {
		y := c.Param(id)
		coll := mg.Database("Flamewave").Collection("cards")
		x := coll.FindOne(cx, bson.D{{Key: id, Value: y}})
		var l FlamewaveTTSCard
		x.Decode(l)
		var card = tabletopsimulator.NewSingleCardObject(l.ContainedObjectsEntry.Nickname, l.ContainedObjectsEntry.Description, l.ContainedObjectsEntry.Memo, l.CustomDeckEntry, false)
		card.States = l.ContainedObjectsEntry.States
		card.LuaScript = l.ContainedObjectsEntry.LuaScript
		c.JSON(200, &card)
	}
}

func getSet(cx context.Context, mg *mongo.Client) gin.HandlerFunc {
	return func(c *gin.Context) {
		y := c.Param("id")
		coll := mg.Database("Flamewave").Collection("cards")
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

func getSetWebsite(cx context.Context, mg *mongo.Client) gin.HandlerFunc {
	return func(c *gin.Context) {
		y := c.Param("id")
		coll := mg.Database("Flamewave").Collection("cards")
		x, e := coll.Find(cx, bson.D{{Key: "set", Value: y}})
		if e != nil {
			return
		}
		var l []FlamewaveTTSCard
		x.All(cx, &l)
		c.JSON(200, &l)
	}
}

func getCollection(cx context.Context, mg *mongo.Client) gin.HandlerFunc {
	return func(c *gin.Context) {
		var identifiers []FlamewaveIdentifier
		c.BindJSON(&identifiers)
		if len(identifiers) == 0 || len(identifiers) > 1000 {
			return
		}
		coll := mg.Database("Flamewave").Collection("cards")
		lstRequests := make(bson.A, len(identifiers))
		for i, thing := range identifiers {
			if thing.FlamewaveId != "" {
				lstRequests[i] = bson.M{"flamewave_id": thing.FlamewaveId}
			} else if thing.ScryfallId != "" {
				lstRequests[i] = bson.M{"scryfall_id": thing.ScryfallId}
			} else if thing.CollectorNumber != "" && thing.SetCode != "" {
				lstRequests[i] = bson.M{
					"cn":  thing.CollectorNumber,
					"set": thing.SetCode,
				}
			} else if thing.OracleId != "" {
				lstRequests[i] = bson.M{"oracle_id": thing.OracleId}
			} else {
				c.JSON(http.StatusBadRequest, "One or more identifiers failed.")
				return
			}
		}
		x, err := coll.Find(cx, bson.M{"$or": lstRequests}, options.Find())
		if err != nil {
			log.Fatal(err)
		}
		var l []FlamewaveTTSCard
		err = x.All(context.TODO(), &l)
		if err != nil {
			log.Fatal(err)
		}
		outputMap := make(map[string]IntermediateCardStruct)
		for _, c := range l {
			for x, identity := range identifiers {
				if len(identity.OracleId) > 0 && identity.OracleId == c.OracleID {
					if o, err := outputMap[c.OracleID]; !err {
						if !o.Priority {
							outputMap[c.OracleID] = IntermediateCardStruct{Card: c, Priority: false}
						}
					} else {
						outputMap[c.OracleID] = IntermediateCardStruct{Card: c, Priority: false}
					}
				} else if (identity.CollectorNumber == c.CollectorNumber && identity.SetCode == c.SetCode) || identity.ScryfallId == c.ScryfallID || identity.FlamewaveId == c.FlamewaveID {
					outputMap[c.OracleID] = IntermediateCardStruct{Card: c, Priority: true}
					identifiers[x].OracleId = c.OracleID
				}
			}
		}
		var deck = tabletopsimulator.NewDeckObject()
		for n, i := range identifiers {
			var c = outputMap[i.OracleId].Card.ContainedObjectsEntry
			if i.Foil {
				c.Decals = []tabletopsimulator.Decal{
					{
						CustomDecal: struct {
							Name     string  "json:\"Name\""
							ImageURL string  "json:\"ImageURL\""
							Size     float32 "json:\"Size\""
						}{Name: "StarFoil", ImageURL: "https://i.imgur.com/QnxyMMK.png", Size: 1.0}, Transform: tabletopsimulator.ExhaustiveTransform{
							PosX:   0.0,
							PosY:   0.25,
							PosZ:   0.0,
							RotX:   90.0,
							RotY:   180.0,
							RotZ:   0.0,
							ScaleX: 0.7006438 * 3.1,
							ScaleY: 0.9999966 * 3.1,
							ScaleZ: 15.3846169 * 3.1,
						}},
				}
			}
			deck.ContainedObjects = append(deck.ContainedObjects, c)
			deck.DeckIDs = append(deck.DeckIDs, int((n+1)*100))
			deck.CustomDeck[fmt.Sprintf("%d", n+1)] = outputMap[i.OracleId].Card.CustomDeckEntry
		}
		c.JSON(http.StatusOK, &deck)
	}
}

func getSets(cx context.Context, mg *mongo.Client) gin.HandlerFunc {
	return func(c *gin.Context) {
		results, err := mg.Database("Flamewave").Collection("cards").Distinct(cx, "set", nil)
		if err != nil {
			c.JSON(http.StatusInternalServerError, "")
		}
		c.JSON(http.StatusOK, results)
	}
}

func getCubeCobra(cx context.Context, mg *mongo.Client) gin.HandlerFunc {
	return func(c *gin.Context) {
		y := c.Param("id")
		coll := mg.Database("Flamewave").Collection("cards")
		client := http.Client{}
		req, err := http.NewRequest(http.MethodGet, fmt.Sprintf("https://cubecobra.com/cube/api/cubeJSON/%v", y), nil)
		if err != nil {
			log.Fatal(err)
		}
		req.Header.Set("User-Agent", "CERA Golang-1.22")
		res, geter := client.Do(req)
		if geter != nil {
			log.Fatal(geter)
		}
		if res.Body != nil {
			defer res.Body.Close()
		}
		var cobra_data CubeCobraResponse
		dec := json.NewDecoder(res.Body)
		dec.Decode(&cobra_data)
		lstSFID := make(bson.A, len(cobra_data.Cards.Mainboard))
		for mainboardindex, mainboardCard := range cobra_data.Cards.Mainboard {
			lstSFID[mainboardindex] = mainboardCard.Details.Scryfall_id
		}
		mongoresponse, err := coll.Find(cx, bson.M{"scryfall_id": bson.M{"$in": lstSFID}}, options.Find())
		if err != nil {
			log.Fatal(err)
		}
		var mongocards []FlamewaveTTSCard
		err = mongoresponse.All(cx, &mongocards)
		if err != nil {
			panic(err)
		}
		outputMap := make(map[string]FlamewaveTTSCard)
		for _, mongocard := range mongocards {
			outputMap[mongocard.ScryfallID] = mongocard
		}
		var deck = tabletopsimulator.NewDeckObject()
		for cobracard_index, cobracard := range cobra_data.Cards.Mainboard {
			deck.ContainedObjects = append(deck.ContainedObjects, outputMap[cobracard.Details.Scryfall_id].ContainedObjectsEntry)
			deck.DeckIDs = append(deck.DeckIDs, int((cobracard_index+1)*100))
			deck.CustomDeck[fmt.Sprintf("%d", cobracard_index+1)] = outputMap[cobracard.Details.Scryfall_id].CustomDeckEntry
		}
		c.JSON(http.StatusOK, &deck)
	}
}
