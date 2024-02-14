package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"

	scryfall "github.com/BlueMonday/go-scryfall"
	"github.com/gin-gonic/gin"
)

const RotatedViewAngleScript = "function onLoad()self.alt_view_angle=Vector(180,0,90)end"
const FlippedViewAngleScript = "function onLoad()self.alt_view_angle=Vector(180,0,180)end"

type Transform struct {
	ScaleX float32 `json:"scaleX"`
	ScaleY float32 `json:"scaleY"`
	ScaleZ float32 `json:"scaleZ"`
}

func OracleTexter(s string) string {
	s = strings.Replace(s, "(", "[i](", -1)
	s = strings.Replace(s, ")", ")[/i]", -1)
	return s
}
func RarityTexter(s string) string {
	switch s {
	case "common":
		return "[ffffff]⌈C⌋[-]"
	case "uncommon":
		return "[6c848c]⌈U⌋[-]"
	case "rare":
		return "[c5b37c]⌈R⌋[-]"
	case "mythic":
		return "[f64800]⌈M⌋[-]"
	case "special":
		return "[905d98]⌈S⌋[-]"
	case "bonus":
		return "[9c202b]⌈B⌋[-]"
	default:
		return "[9c202b]⌈B⌋[-]"
	}
}

type Identifier struct {
	ScryfallId      string `json:"scryfall_id"`
	OracleId        string `json:"oracle_id"`
	CollectorNumber string `json:"cn"`
	SetCode         string `json:"set"`
	Quantity        uint8  `json:"quantity"`
}

type IntermediateCard struct {
	Card     FlamewaveTTSCard
	Priority bool
}

func getStuff(c *gin.Context) {
	var stuff []Identifier
	stuff = append(stuff, Identifier{ScryfallId: "4d3f41dc-72f6-4346-b95f-4813addb5af0"})
	stuff = append(stuff, Identifier{CollectorNumber: "1", SetCode: "lea", Quantity: 4})
	stuff = append(stuff, Identifier{OracleId: "ca00eb17-e5c3-42c8-a665-431f5f95b67f"})
	f, err := os.Open("default-cards.json")
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
	outputMap := make(map[string]IntermediateCard)
	var deck = NewEmptyDeckObject()
	for _, c := range l {
		for x, identity := range stuff {
			if len(identity.OracleId) > 0 && identity.OracleId == c.OracleID {
				if o, err := outputMap[c.OracleID]; !err {
					if !o.Priority {
						outputMap[c.OracleID] = IntermediateCard{Card: c, Priority: false}
					}
				}
			}
			if (identity.CollectorNumber == c.CollectorNumber && identity.SetCode == c.SetCode) || identity.ScryfallId == c.ScryfallID {
				outputMap[c.OracleID] = IntermediateCard{Card: c, Priority: true}
				stuff[x].OracleId = c.OracleID
			}
		}
	}
	for _, i := range stuff {
		for q := 0; q <= int(i.Quantity); q++ {
			var c = outputMap[i.OracleId]
			deck.ContainedObjects = append(deck.ContainedObjects, c.Card.ContainedObjectsEntry)
			deck.DeckIDs = append(deck.DeckIDs, int(c.Card.DeckIDEntry))
			deck.CustomDeck[c.Card.CustomDeckID] = c.Card.CustomDeckEntry
		}
	}
	// outputSave := TTSSave{ObjectStates: []TTSDeckObject{deck}}
	c.JSON(http.StatusOK, deck)
}

func main() {
	ctx := context.Background()
	client, err := scryfall.NewClient()
	if err != nil {
		log.Fatal(err)
	}
	router := gin.Default()
	router.GET("/", getStuff)
	// router.GET("/playground", getStuff) // There's also a JSON representation for stuff here.
	// router.GET("/simulator", getStuff)  // Returns full JSON string for spawning an object. Pass directly into spawnObjectData.
	router.POST("/simulator/collection", getStuff)
	router.GET("/update", updateBulk(ctx, client))
	router.Run("localhost:8080")
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
					outList = append(outList, NewFWCard(m, counter))
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
func NewEmptyDeckObject() TTSDeckObject {
	var w = TTSDeckObject{Name: "Deck", Transform: Transform{ScaleX: 1.0, ScaleY: 1.0, ScaleZ: 1.0}, DeckIDs: []int{}, ContainedObjects: []TTSCardObjectEntry{}, CustomDeck: make(map[string]TTSImageEntry)}
	return w
}

type TTSSave struct {
	ObjectStates []TTSDeckObject `json:"ObjectStates"`
}

type TTSDeckObject struct {
	Name             string                   `json:"Name"`
	Transform        Transform                `json:"Transform"`
	DeckIDs          []int                    `json:"DeckIDs"`
	ContainedObjects []TTSCardObjectEntry     `json:"ContainedObjects"`
	CustomDeck       map[string]TTSImageEntry `json:"CustomDeck"`
}

type TTSImageEntry struct {
	FaceURL      string `json:"FaceURL"`
	BackURL      string `json:"BackURL"`
	NumWidth     uint8  `json:"NumWidth"`
	NumHeight    uint8  `json:"NumHeight"`
	BackIsHidden bool   `json:"BackIsHidden"`
}

type TTSStateEntry struct {
	CustomDeck  map[string]TTSImageEntry `json:"CustomDeck"`
	Name        string                   `json:"Name"`
	Transform   Transform                `json:"Transform"`
	Nickname    string                   `json:"Nickname"`
	Description string                   `json:"Description"`
	Memo        string                   `json:"Memo"`
	CardID      uint32                   `json:"CardID"`
	LuaScript   string                   `json:"LuaScript"`
}

type TTSCardObjectEntry struct {
	Name        string                   `json:"Name"`
	Transform   Transform                `json:"Transform"`
	Nickname    string                   `json:"Nickname"`
	Description string                   `json:"Description"`
	Memo        string                   `json:"Memo"`
	States      map[string]TTSStateEntry `json:"States"`
	LuaScript   string                   `json:"LuaScript"`
}

type FlamewaveTTSCard struct {
	CollectorNumber       string             `json:"CollectorNumber"`
	SetCode               string             `json:"SetCode"`
	OracleID              string             `json:"OracleID"`
	ScryfallID            string             `json:"ScryfallID"`
	DeckIDEntry           uint32             `json:"DeckIDEntry"`
	CustomDeckID          string             `json:"CustomDeckID"`
	CustomDeckEntry       TTSImageEntry      `json:"CustomDeckEntry"`
	ContainedObjectsEntry TTSCardObjectEntry `json:"ContainedObjectsEntry"`
}

func NewFWCard(c scryfall.Card, i uint32) FlamewaveTTSCard {
	var FWCard = FlamewaveTTSCard{
		CollectorNumber:       c.CollectorNumber,
		SetCode:               c.Set,
		OracleID:              c.OracleID,
		ScryfallID:            c.ID,
		DeckIDEntry:           i * 100,
		CustomDeckID:          fmt.Sprintf("%d", i),
		CustomDeckEntry:       TTSImageEntry{},
		ContainedObjectsEntry: TTSCardObjectEntry{},
	}
	var CustomDeckEntry TTSImageEntry = TTSImageEntry{
		FaceURL:      "",
		BackURL:      "https://i.imgur.com/TyC0LWj.jpg",
		NumWidth:     1,
		NumHeight:    1,
		BackIsHidden: true,
	}
	var ContainedObjectsEntry TTSCardObjectEntry = TTSCardObjectEntry{
		States:      map[string]TTSStateEntry{},
		Name:        "Card",
		Transform:   Transform{ScaleX: 1, ScaleY: 1, ScaleZ: 1},
		Nickname:    "",
		Description: "",
		Memo:        "",
		LuaScript:   "",
	}
	if len(c.OracleID) == 0 {
		ContainedObjectsEntry.Memo = *c.CardFaces[0].OracleID
	} else {
		ContainedObjectsEntry.Memo = c.OracleID
	}
	if c.Layout == scryfall.LayoutNormal || c.Layout == scryfall.LayoutLeveler || c.Layout == scryfall.LayoutMeld || c.Layout == scryfall.LayoutSaga || c.Layout == scryfall.LayoutToken || c.Layout == scryfall.LayoutHost || c.Layout == scryfall.LayoutAugment || c.Layout == scryfall.LayoutEmblem || c.Layout == scryfall.LayoutPrototype || c.Layout == scryfall.LayoutMutate || c.Layout == scryfall.LayoutCase || c.Layout == scryfall.LayoutClass {
		var descriptionbuffer bytes.Buffer
		descriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.Name, c.ManaCost, c.TypeLine, RarityTexter(c.Rarity), OracleTexter(c.OracleText)))
		if c.Power != nil {
			descriptionbuffer.WriteString(fmt.Sprintf("\n%s/%s", *c.Power, *c.Toughness))
		}
		if c.Loyalty != nil {
			descriptionbuffer.WriteString(fmt.Sprintf("\nLoyalty: %s", *c.Loyalty))
		}
		ContainedObjectsEntry.Description = descriptionbuffer.String()
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %dMV", c.Name, c.TypeLine, uint8(c.CMC)))
		ContainedObjectsEntry.Nickname = namebuffer.String()
		CustomDeckEntry.FaceURL = c.ImageURIs.Normal
	}
	if c.Layout == scryfall.LayoutSplit {
		var descriptionbuffer bytes.Buffer
		descriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[0].Name, c.CardFaces[0].ManaCost, c.CardFaces[0].TypeLine, RarityTexter(c.Rarity), OracleTexter(*c.CardFaces[0].OracleText)))
		descriptionbuffer.WriteString(fmt.Sprintf("\n[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[1].Name, c.CardFaces[1].ManaCost, c.CardFaces[1].TypeLine, RarityTexter(c.Rarity), OracleTexter(*c.CardFaces[1].OracleText)))
		ContainedObjectsEntry.Description = descriptionbuffer.String()
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %dMV", c.Name, c.TypeLine, uint8(c.CMC)))
		ContainedObjectsEntry.LuaScript = RotatedViewAngleScript
		ContainedObjectsEntry.Nickname = namebuffer.String()
		CustomDeckEntry.FaceURL = c.ImageURIs.Normal
	}
	if c.Layout == scryfall.LayoutFlip {
		var frontdescriptionbuffer bytes.Buffer
		frontdescriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[0].Name, c.CardFaces[0].ManaCost, c.CardFaces[0].TypeLine, RarityTexter(c.Rarity), OracleTexter(*c.CardFaces[0].OracleText)))
		if c.CardFaces[0].Power != nil && c.CardFaces[0].Toughness != nil {
			frontdescriptionbuffer.WriteString(fmt.Sprintf("\n%s/%s", *c.CardFaces[0].Power, *c.CardFaces[0].Toughness))
		}
		var backdescriptionbuffer bytes.Buffer
		backdescriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[1].Name, c.CardFaces[1].ManaCost, c.CardFaces[1].TypeLine, RarityTexter(c.Rarity), OracleTexter(*c.CardFaces[1].OracleText)))
		if c.CardFaces[1].Power != nil && c.CardFaces[1].Toughness != nil {
			backdescriptionbuffer.WriteString(fmt.Sprintf("\n%s/%s", *c.CardFaces[1].Power, *c.CardFaces[1].Toughness))
		}
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %fMV", c.Name, c.TypeLine, c.CMC))
		ContainedObjectsEntry.Nickname = namebuffer.String()
		if strings.Contains(c.CardFaces[0].TypeLine, "Battle") {
			ContainedObjectsEntry.LuaScript = RotatedViewAngleScript
		}
		CustomDeckEntry.FaceURL = c.ImageURIs.Normal
		ContainedObjectsEntry.Description = fmt.Sprintf("%s\n[6E6E6E]%s[-]", frontdescriptionbuffer.String(), backdescriptionbuffer.String())
		// The States indices are mutually exclusive to the outer deck. It's safe to use 100.
		ContainedObjectsEntry.States["2"] = TTSStateEntry{
			Name:        "Card",
			Transform:   Transform{ScaleX: 1.0, ScaleY: 1.0, ScaleZ: 1.0},
			CardID:      100,
			Nickname:    namebuffer.String(),
			Description: fmt.Sprintf("[6E6E6E]%s[-]\n%s", frontdescriptionbuffer.String(), backdescriptionbuffer.String()),
			Memo:        c.OracleID,
			LuaScript:   FlippedViewAngleScript,
			CustomDeck: map[string]TTSImageEntry{
				"100": {
					FaceURL:      c.ImageURIs.Normal,
					BackURL:      "https://i.imgur.com/TyC0LWj.jpg",
					NumWidth:     1,
					NumHeight:    1,
					BackIsHidden: true,
				},
			},
		}
	}
	if c.Layout == scryfall.LayoutTransform || c.Layout == scryfall.LayoutDoubleFacedToken || c.Layout == scryfall.LayoutModalDFC || c.Layout == scryfall.LayoutReversible || c.Layout == scryfall.LayoutArtSeries {
		var frontdescriptionbuffer bytes.Buffer
		frontdescriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[0].Name, c.CardFaces[0].ManaCost, c.CardFaces[0].TypeLine, RarityTexter(c.Rarity), OracleTexter(*c.CardFaces[0].OracleText)))
		if c.CardFaces[0].Power != nil && c.CardFaces[0].Toughness != nil {
			frontdescriptionbuffer.WriteString(fmt.Sprintf("\n%s/%s", *c.CardFaces[0].Power, *c.CardFaces[0].Toughness))
		}
		if c.CardFaces[0].Loyalty != nil {
			frontdescriptionbuffer.WriteString(fmt.Sprintf("\nLoyalty: %s", *c.CardFaces[0].Loyalty))
		}
		if c.CardFaces[0].Defense != nil {
			frontdescriptionbuffer.WriteString(fmt.Sprintf("\nDefense: %s", *c.CardFaces[0].Defense))
		}
		var backdescriptionbuffer bytes.Buffer
		backdescriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[1].Name, c.CardFaces[1].ManaCost, c.CardFaces[1].TypeLine, RarityTexter(c.Rarity), OracleTexter(*c.CardFaces[1].OracleText)))
		if c.CardFaces[1].Power != nil && c.CardFaces[1].Toughness != nil {
			backdescriptionbuffer.WriteString(fmt.Sprintf("\n%s/%s", *c.CardFaces[1].Power, *c.CardFaces[1].Toughness))
		}
		if c.CardFaces[1].Loyalty != nil {
			backdescriptionbuffer.WriteString(fmt.Sprintf("\nLoyalty: %s", *c.CardFaces[1].Loyalty))
		}
		if c.CardFaces[0].Defense != nil {
			frontdescriptionbuffer.WriteString(fmt.Sprintf("\nDefense: %s", *c.CardFaces[0].Defense))
		}
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %dMV", c.Name, c.TypeLine, uint8(c.CMC)))
		ContainedObjectsEntry.Nickname = namebuffer.String()
		if strings.Contains(c.CardFaces[0].TypeLine, "Battle") {
			ContainedObjectsEntry.LuaScript = RotatedViewAngleScript
		}
		CustomDeckEntry.FaceURL = c.CardFaces[0].ImageURIs.Normal
		ContainedObjectsEntry.Description = fmt.Sprintf("%s\n[6E6E6E]%s[-]", frontdescriptionbuffer.String(), backdescriptionbuffer.String())
		// The States indices are mutually exclusive to the outer deck. It's safe to use 100.
		ContainedObjectsEntry.States["2"] = TTSStateEntry{
			Name:        "Card",
			Transform:   Transform{ScaleX: 1.0, ScaleY: 1.0, ScaleZ: 1.0},
			CardID:      100,
			Nickname:    namebuffer.String(),
			Description: fmt.Sprintf("[6E6E6E]%s[-]\n%s", frontdescriptionbuffer.String(), backdescriptionbuffer.String()),
			Memo:        c.OracleID,
			LuaScript:   "",
			CustomDeck: map[string]TTSImageEntry{
				"100": {
					FaceURL:      c.CardFaces[1].ImageURIs.Normal,
					BackURL:      "https://i.imgur.com/TyC0LWj.jpg",
					NumWidth:     1,
					NumHeight:    1,
					BackIsHidden: true,
				},
			},
		}
	}
	if c.Layout == scryfall.LayoutAdventure {
		var descriptionbuffer bytes.Buffer
		descriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[0].Name, c.CardFaces[0].ManaCost, c.CardFaces[0].TypeLine, RarityTexter(c.Rarity), OracleTexter(*c.CardFaces[0].OracleText)))
		if c.Power != nil && c.Toughness != nil {
			descriptionbuffer.WriteString(fmt.Sprintf("\n%s/%s", *c.Power, *c.Toughness))
		}
		descriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[1].Name, c.CardFaces[1].ManaCost, c.CardFaces[1].TypeLine, RarityTexter(c.Rarity), OracleTexter(*c.CardFaces[1].OracleText)))
		ContainedObjectsEntry.Description = descriptionbuffer.String()
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %dMV", c.Name, c.TypeLine, uint8(c.CMC)))
		ContainedObjectsEntry.Nickname = namebuffer.String()
		CustomDeckEntry.FaceURL = c.ImageURIs.Normal
	}
	if c.Layout == scryfall.LayoutBattle {
		// No cards exist with this layout.
	}
	if c.Layout == scryfall.LayoutPlanar {
		var descriptionbuffer bytes.Buffer
		descriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.Name, c.ManaCost, c.TypeLine, RarityTexter(c.Rarity), OracleTexter(c.OracleText)))
		ContainedObjectsEntry.Description = descriptionbuffer.String()
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %dMV", c.Name, c.TypeLine, uint8(c.CMC)))
		ContainedObjectsEntry.Nickname = namebuffer.String()
		ContainedObjectsEntry.LuaScript = RotatedViewAngleScript
		CustomDeckEntry.FaceURL = c.ImageURIs.Normal
	}
	if c.Layout == scryfall.LayoutScheme {
		var descriptionbuffer bytes.Buffer
		descriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.Name, c.ManaCost, c.TypeLine, RarityTexter(c.Rarity), OracleTexter(c.OracleText)))
		ContainedObjectsEntry.Description = descriptionbuffer.String()
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %dMV", c.Name, c.TypeLine, uint8(c.CMC)))
		ContainedObjectsEntry.Nickname = namebuffer.String()
		CustomDeckEntry.FaceURL = c.ImageURIs.Normal
	}
	if c.Layout == scryfall.LayoutVanguard {
		var descriptionbuffer bytes.Buffer
		descriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.Name, c.ManaCost, c.TypeLine, RarityTexter(c.Rarity), OracleTexter(c.OracleText)))
		descriptionbuffer.WriteString(fmt.Sprintf("\nHand Modifier: %s\nLife Modifier: %s", *c.HandModifier, *c.LifeModifier))
		ContainedObjectsEntry.Description = descriptionbuffer.String()
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %dMV", c.Name, c.TypeLine, uint8(c.CMC)))
		ContainedObjectsEntry.Nickname = namebuffer.String()
		CustomDeckEntry.FaceURL = c.ImageURIs.Normal
	}
	FWCard.ContainedObjectsEntry = ContainedObjectsEntry
	FWCard.CustomDeckEntry = CustomDeckEntry
	return FWCard
}
