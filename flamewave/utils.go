package main

import (
	"bytes"
	tabletopsimulator "flamewave/tabletopsimulator"
	"fmt"
	"strings"

	scryfall "github.com/BlueMonday/go-scryfall"
)

const RotatedViewAngleScript = "function onLoad()self.alt_view_angle=Vector(180,0,90)end"
const FlippedViewAngleScript = "function onLoad()self.alt_view_angle=Vector(180,0,180)end"

func OracleBBCodeTexter(s string) string {
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

type FlamewaveIdentifier struct {
	ScryfallId      string `json:"scryfall_id"`
	OracleId        string `json:"oracle_id"`
	CollectorNumber string `json:"cn"`
	SetCode         string `json:"set"`
	Quantity        uint8  `json:"quantity"`
	FlamewaveId     string `json:"flamewave_id"`
}

type FlamewaveTTSCard struct {
	CollectorNumber       string                      `json:"CollectorNumber"`
	SetCode               string                      `json:"SetCode"`
	OracleID              string                      `json:"OracleID"`
	ScryfallID            string                      `json:"ScryfallID"`
	FlamewaveID           string                      `json:"FlamewaveID"`
	CustomDeckEntry       tabletopsimulator.CardImage `json:"CustomDeckEntry"`
	ContainedObjectsEntry tabletopsimulator.Card      `json:"ContainedObjectsEntry"`
}

func NewFlamewaveTTSCard(c scryfall.Card, i uint32) FlamewaveTTSCard {
	var faceURL = ""
	var nickName = ""
	var description = ""
	var memo = ""
	var luaScript = ""
	var extraState = false
	var additionalState tabletopsimulator.CardState

	if len(c.OracleID) == 0 {
		memo = *c.CardFaces[0].OracleID
	} else {
		memo = c.OracleID
	}
	if c.Layout == scryfall.LayoutNormal || c.Layout == scryfall.LayoutLeveler || c.Layout == scryfall.LayoutMeld || c.Layout == scryfall.LayoutSaga || c.Layout == scryfall.LayoutToken || c.Layout == scryfall.LayoutHost || c.Layout == scryfall.LayoutAugment || c.Layout == scryfall.LayoutEmblem || c.Layout == scryfall.LayoutPrototype || c.Layout == scryfall.LayoutMutate || c.Layout == scryfall.LayoutCase || c.Layout == scryfall.LayoutClass {
		var descriptionbuffer bytes.Buffer
		descriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.Name, c.ManaCost, c.TypeLine, RarityTexter(c.Rarity), OracleBBCodeTexter(c.OracleText)))
		if c.Power != nil {
			descriptionbuffer.WriteString(fmt.Sprintf("\n%s/%s", *c.Power, *c.Toughness))
		}
		if c.Loyalty != nil {
			descriptionbuffer.WriteString(fmt.Sprintf("\nLoyalty: %s", *c.Loyalty))
		}
		description = descriptionbuffer.String()
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %dMV", c.Name, c.TypeLine, uint8(c.CMC)))
		nickName = namebuffer.String()
		faceURL = c.ImageURIs.Normal
	}
	if c.Layout == scryfall.LayoutSplit {
		var descriptionbuffer bytes.Buffer
		descriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[0].Name, c.CardFaces[0].ManaCost, c.CardFaces[0].TypeLine, RarityTexter(c.Rarity), OracleBBCodeTexter(*c.CardFaces[0].OracleText)))
		descriptionbuffer.WriteString(fmt.Sprintf("\n[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[1].Name, c.CardFaces[1].ManaCost, c.CardFaces[1].TypeLine, RarityTexter(c.Rarity), OracleBBCodeTexter(*c.CardFaces[1].OracleText)))
		description = descriptionbuffer.String()
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %dMV", c.Name, c.TypeLine, uint8(c.CMC)))
		luaScript = RotatedViewAngleScript
		nickName = namebuffer.String()
		faceURL = c.ImageURIs.Normal
	}
	if c.Layout == scryfall.LayoutFlip {
		var frontdescriptionbuffer bytes.Buffer
		frontdescriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[0].Name, c.CardFaces[0].ManaCost, c.CardFaces[0].TypeLine, RarityTexter(c.Rarity), OracleBBCodeTexter(*c.CardFaces[0].OracleText)))
		if c.CardFaces[0].Power != nil && c.CardFaces[0].Toughness != nil {
			frontdescriptionbuffer.WriteString(fmt.Sprintf("\n%s/%s", *c.CardFaces[0].Power, *c.CardFaces[0].Toughness))
		}
		var backdescriptionbuffer bytes.Buffer
		backdescriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[1].Name, c.CardFaces[1].ManaCost, c.CardFaces[1].TypeLine, RarityTexter(c.Rarity), OracleBBCodeTexter(*c.CardFaces[1].OracleText)))
		if c.CardFaces[1].Power != nil && c.CardFaces[1].Toughness != nil {
			backdescriptionbuffer.WriteString(fmt.Sprintf("\n%s/%s", *c.CardFaces[1].Power, *c.CardFaces[1].Toughness))
		}
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %fMV", c.Name, c.TypeLine, c.CMC))
		nickName = namebuffer.String()
		if strings.Contains(c.CardFaces[0].TypeLine, "Battle") {
			luaScript = RotatedViewAngleScript
		}
		faceURL = c.ImageURIs.Normal
		description = fmt.Sprintf("%s\n[6E6E6E]%s[-]", frontdescriptionbuffer.String(), backdescriptionbuffer.String())
		extraState = true
		// The States indices are mutually exclusive to the outer deck. It's safe to use 100.
		additionalState = tabletopsimulator.NewStateEntry(namebuffer.String(), fmt.Sprintf("[6E6E6E]%s[-]\n%s", frontdescriptionbuffer.String(), backdescriptionbuffer.String()), c.OracleID, FlippedViewAngleScript, tabletopsimulator.NewImageEntry(c.ImageURIs.Normal, "https://i.imgur.com/TyC0LWj.jpg"))
	}
	if c.Layout == scryfall.LayoutTransform || c.Layout == scryfall.LayoutDoubleFacedToken || c.Layout == scryfall.LayoutModalDFC || c.Layout == scryfall.LayoutReversible || c.Layout == scryfall.LayoutArtSeries {
		var frontdescriptionbuffer bytes.Buffer
		frontdescriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[0].Name, c.CardFaces[0].ManaCost, c.CardFaces[0].TypeLine, RarityTexter(c.Rarity), OracleBBCodeTexter(*c.CardFaces[0].OracleText)))
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
		backdescriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[1].Name, c.CardFaces[1].ManaCost, c.CardFaces[1].TypeLine, RarityTexter(c.Rarity), OracleBBCodeTexter(*c.CardFaces[1].OracleText)))
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
		nickName = namebuffer.String()
		if strings.Contains(c.CardFaces[0].TypeLine, "Battle") {
			luaScript = RotatedViewAngleScript
		}
		faceURL = c.CardFaces[0].ImageURIs.Normal
		description = fmt.Sprintf("%s\n[6E6E6E]%s[-]", frontdescriptionbuffer.String(), backdescriptionbuffer.String())
		extraState = true
		// The States indices are mutually exclusive to the outer deck. It's safe to use 100.
		additionalState = tabletopsimulator.NewStateEntry(namebuffer.String(), fmt.Sprintf("[6E6E6E]%s[-]\n%s", frontdescriptionbuffer.String(), backdescriptionbuffer.String()), c.OracleID, "", tabletopsimulator.NewImageEntry(c.CardFaces[1].ImageURIs.Normal, "https://i.imgur.com/TyC0LWj.jpg"))
	}
	if c.Layout == scryfall.LayoutAdventure {
		var descriptionbuffer bytes.Buffer
		descriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[0].Name, c.CardFaces[0].ManaCost, c.CardFaces[0].TypeLine, RarityTexter(c.Rarity), OracleBBCodeTexter(*c.CardFaces[0].OracleText)))
		if c.Power != nil && c.Toughness != nil {
			descriptionbuffer.WriteString(fmt.Sprintf("\n%s/%s", *c.Power, *c.Toughness))
		}
		descriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[1].Name, c.CardFaces[1].ManaCost, c.CardFaces[1].TypeLine, RarityTexter(c.Rarity), OracleBBCodeTexter(*c.CardFaces[1].OracleText)))
		description = descriptionbuffer.String()
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %dMV", c.Name, c.TypeLine, uint8(c.CMC)))
		nickName = namebuffer.String()
		faceURL = c.ImageURIs.Normal
	}
	// if c.Layout == scryfall.LayoutBattle {
	// No cards exist with this layout.
	// }
	if c.Layout == scryfall.LayoutPlanar {
		var descriptionbuffer bytes.Buffer
		descriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.Name, c.ManaCost, c.TypeLine, RarityTexter(c.Rarity), OracleBBCodeTexter(c.OracleText)))
		description = descriptionbuffer.String()
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %dMV", c.Name, c.TypeLine, uint8(c.CMC)))
		nickName = namebuffer.String()
		luaScript = RotatedViewAngleScript
		faceURL = c.ImageURIs.Normal
	}
	if c.Layout == scryfall.LayoutScheme {
		var descriptionbuffer bytes.Buffer
		descriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.Name, c.ManaCost, c.TypeLine, RarityTexter(c.Rarity), OracleBBCodeTexter(c.OracleText)))
		description = descriptionbuffer.String()
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %dMV", c.Name, c.TypeLine, uint8(c.CMC)))
		nickName = namebuffer.String()
		faceURL = c.ImageURIs.Normal
	}
	if c.Layout == scryfall.LayoutVanguard {
		var descriptionbuffer bytes.Buffer
		descriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.Name, c.ManaCost, c.TypeLine, RarityTexter(c.Rarity), OracleBBCodeTexter(c.OracleText)))
		descriptionbuffer.WriteString(fmt.Sprintf("\nHand Modifier: %s\nLife Modifier: %s", *c.HandModifier, *c.LifeModifier))
		description = descriptionbuffer.String()
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %dMV", c.Name, c.TypeLine, uint8(c.CMC)))
		nickName = namebuffer.String()
		faceURL = c.ImageURIs.Normal
	}
	var FWCard = FlamewaveTTSCard{
		CollectorNumber:       c.CollectorNumber,
		SetCode:               c.Set,
		OracleID:              c.OracleID,
		ScryfallID:            c.ID,
		FlamewaveID:           c.ID,
		CustomDeckEntry:       tabletopsimulator.NewImageEntry(faceURL, "https://i.imgur.com/TyC0LWj.jpg"),
		ContainedObjectsEntry: tabletopsimulator.Card{},
	}
	var ContainedObjectsEntry tabletopsimulator.Card = tabletopsimulator.NewCardEntry(nickName, description, memo)
	ContainedObjectsEntry.LuaScript = luaScript
	if extraState {
		ContainedObjectsEntry.States["2"] = additionalState
	}
	FWCard.ContainedObjectsEntry = ContainedObjectsEntry
	return FWCard
}
