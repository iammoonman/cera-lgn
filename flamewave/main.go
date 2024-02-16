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

	scryfall "github.com/BlueMonday/go-scryfall"
	"github.com/gin-gonic/gin"
)

func main() {
	ctx := context.Background()
	client, err := scryfall.NewClient()
	if err != nil {
		log.Fatal(err)
	}
	router := gin.Default()
	router.GET("/", postCollection)
	// router.GET("/playground", getStuff) // There's also a JSON representation for stuff here.
	// router.GET("/simulator", getStuff)  // Returns full JSON string for spawning an object. Pass directly into spawnObjectData.
	router.POST("/simulator/collection", postCollection)
	router.GET("/update", updateBulk(ctx, client))
	router.Run("localhost:8080")
}

type IntermediateCardStruct struct {
	Card     FlamewaveTTSCard
	Priority bool
}

func postCollection(c *gin.Context) {
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
	f, err := os.Open("default-cards.json")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()
	if err != nil {
		log.Fatal(err)
	}
	if len(stuff) == 0 {
		return
	}
	dec := json.NewDecoder(f)
	var l []FlamewaveTTSCard
	err = dec.Decode(&l)
	if err != nil {
		log.Fatal(err)
	}
	outputMap := make(map[string]IntermediateCardStruct)
	var deck = tabletopsimulator.NewDeckObject()
	for _, c := range l {
		for x, identity := range stuff {
			if len(identity.OracleId) > 0 && identity.OracleId == c.OracleID {
				if o, err := outputMap[c.OracleID]; !err {
					if !o.Priority {
						outputMap[c.OracleID] = IntermediateCardStruct{Card: c, Priority: false}
					}
				}
			}
			if (identity.CollectorNumber == c.CollectorNumber && identity.SetCode == c.SetCode) || identity.ScryfallId == c.ScryfallID {
				outputMap[c.OracleID] = IntermediateCardStruct{Card: c, Priority: true}
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

func updateBulk(cx context.Context, ct *scryfall.Client) gin.HandlerFunc {
	return func(c *gin.Context) {
		bulkList, err := ct.ListBulkData(cx)
		if err != nil {
			log.Fatal(err)
		}
		for _, entry := range bulkList {
			if entry.Type == "default_cards" {
				out, err := os.Create("default-cards.json")
				if err != nil {
					log.Fatal(err)
				}
				defer out.Close()
				resp, err := http.Get(entry.DownloadURI)
				if err != nil {
					log.Fatal(err)
				}
				defer resp.Body.Close()
				// io.Copy(out, resp.Body)
				// Just parse the stuff into TTS format here.
				var outList = []FlamewaveTTSCard{}
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
					outList = append(outList, NewFlamewaveTTSCard(m, counter))
				}
				dec.Token()
				v, err := json.Marshal(outList)
				if err != nil {
					log.Fatal(err)
				}
				_, err = out.Write(v)
				if err != nil {
					log.Fatal(err)
				}
			}
		}
	}
}
