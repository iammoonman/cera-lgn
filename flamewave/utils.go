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
	ScryfallId      string `json:"scryfall_id" bson:"scryfall_id"`
	OracleId        string `json:"oracle_id" bson:"oracle_id"`
	CollectorNumber string `json:"cn" bson:"cn"`
	SetCode         string `json:"set" bson:"set"`
	Quantity        uint8  `json:"quantity" bson:"quantity"`
	FlamewaveId     string `json:"flamewave_id" bson:"flamewave_id"`
}

type FlamewaveTTSCard struct {
	CollectorNumber       string                      `json:"cn" bson:"cn"`
	SetCode               string                      `json:"set" bson:"set"`
	OracleID              string                      `json:"oracle_id" bson:"oracle_id"`
	ScryfallID            string                      `json:"scryfall_id" bson:"scryfall_id"`
	FlamewaveID           string                      `json:"flamewave_id" bson:"flamewave_id"`
	CustomDeckEntry       tabletopsimulator.CardImage `json:"custom_deck" bson:"custom_deck"`
	ContainedObjectsEntry tabletopsimulator.Card      `json:"cotd_objs" bson:"cotd_objs"`
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

var SetCodes []string = []string{
	"tsp", "zen", "tmm2", "xln", "3ed", "who", "woe", "eld", "ugin", "m21", "jmp", "tmp", "dmu", "sld", "me4", "pcy", "plst", "c15", "c18", "f08", "plci", "mom", "ced", "dmr", "prm", "grn", "cns", "nph", "gtc", "ltc", "woc", "tsr", "dom", "m19", "vis", "rvr", "c20", "ody", "isd", "mh2", "arn", "aer", "30a", "mir", "bchr", "mbs", "ncc", "clb", "tvow", "dtk", "fbb", "yone", "ogw", "9ed", "mma", "p02", "vma", "ddm", "cma", "brb", "aznr", "uds", "ltr", "2x2", "7ed", "wc02", "rna", "ema", "ugl", "pal03", "brc", "me2", "m13", "khc", "mm3", "unh", "bfz", "sir", "mm2", "gk1", "ydmu", "c16", "znc", "sok", "pone", "piko", "5ed", "p15a", "pz2", "lci", "akh", "inv", "moc", "mh1", "wc98", "tsb", "pm19", "mid", "4bb", "j22", "anb", "neo", "c21", "snc", "nem", "por", "dmc", "cmm", "pstx", "tsoi", "bok", "hou",
	"2ed", "c17", "ktk", "pjou", "cmb1", "c14", "sis", "psnc", "pkld", "pznr", "stx", "mkm", "8ed", "leb", "mmq", "pm21", "wc01", "akr", "con", "pkhm", "tddj", "cmr", "roe", "ddr", "mat", "cei", "cn2", "frf", "pthb", "csp", "pwar", "znr", "ori", "tmh1", "fut", "ps11", "pdom", "opca", "ymid", "tlci", "dbl", "cmb2", "ps15", "jud", "tc21", "unf", "4ed", "twho", "eve", "prwk", "iko", "phuk", "e02", "ptk", "aone", "j21", "hbg", "10e", "40k", "bro", "tpca", "kld", "rav", "ptc", "lcc", "mic", "ice", "sum", "acmm", "admu", "wmkm", "pmh2", "war", "gk2", "awoe", "avow", "c13", "g06", "nec", "cm2", "f16", "scd", "rix", "all", "gpt", "2xm", "m14", "dst", "som", "pafr", "wc97",
	"6ed", "gn3", "rex", "cmd", "dis", "m12", "pres", "m11", "zne", "wc03", "arb", "onc", "mul", "klr", "tcmm", "chk", "hml", "m20", "clu", "mrd", "opc2", "hop", "rin", "ust", "w16", "afr", "5dn", "ima", "prix", "uma", "fdmu", "tmoc", "tunf", "mor", "vow", "fltr", "j20",
	"pneo", "dds", "pvow", "me1", "h09", "pal00", "ath", "soi", "ha5", "astx", "ths", "usg", "m15", "exp", "one", "pmps", "rtr", "pbro", "tmkc", "sth", "wot", "tor", "tmma", "pmkm", "ha6", "thb", "altr", "sunf", "chr", "ddk", "bng", "fem", "dka", "oc20", "tpr", "pdci", "ttsr", "slc", "gvl", "ddn", "amh1", "wc99", "tkhc", "c19", "pclb", "tc14", "ybro", "t40k", "psal", "scg", "pw22", "wth", "peld", "ddt", "ren", "mps", "amh2", "tclb", "td0", "tznc", "f05", "abro", "apc", "dvd", "wwk", "pemn", "pls", "ala", "tc17", "voc", "tncc", "ulg",
	"dpa", "pmid", "avr", "slu", "emn", "shm", "tltc", "tmkm", "dgm", "exo", "ss1", "mp2", "trna", "a25", "plc", "itp", "alci", "ha3", "pakh", "tneo", "gs1", "pori", "s99", "ddq", "psoi", "tkhm", "afc", "tscd", "tlrw", "td2", "prna", "brr", "w17", "pbfz", "j12", "pd2", "psdg", "phou", "ddh", "p30a", "pmoa", "pmei", "khm", "pvan", "sta", "j14", "tc16", "tonc", "pm20", "pwoe", "olep", "f13", "tktk", "m10", "o90p", "drb", "ddi", "fj22", "leg", "lea", "skhm", "tc15", "ons", "pgtc", "tgrn", "ddg", "ovnt", "bbd", "pca", "ana", "tuma", "tmom", "cm1", "j13", "jvc", "twoc", "jou", "spg", "tmh2", "pbbd", "pidw", "ulst", "aafr", "lrw", "pip", "wc00", "tmm3", "mkc", "tbfz", "pjjt", "ddu", "pz1", "ddf", "aclb", "lgn", "f07", "md1", "ddj", "aneo", "ohop", "dde", "g17", "ea3", "tdd1", "atq", "gn2", "pal04", "f06", "pgrn", "twwk", "cp3", "ha4", "mstx", "pcel", "pltr", "puma", "pxln", "pf19", "psvc", "tm20", "ysnc", "ph22", "oarc", "f17", "pmom", "tdmr", "tcm2", "h1r", "trtr", "pana", "akhm", "ddp", "ph19", "oana", "mneo", "dd1", "tmd1", "arc", "btd", "tgn3", "sstx", "tshm", "l12", "pdtk", "me3", "pdp12", "tmed", "v11", "cst", "tmor", "amom", "pw24", "pc2", "drk", "asnc", "wc04", "ha2", "pd3", "pktk", "e01", "tcmr", "t2xm", "tsnc", "pss3", "temn", "pal06", "pwcs", "tznr", "slp", "tc20", "ddl", "ta25", "med", "ocmd", "v10", "tc18", "pdmu",
	"p07", "tdag", "pf20", "tm21", "pl23", "pm14", "teve", "pplc", "tm19", "takh", "prtr", "ywoe", "amid", "tm14", "ha7", "olgc", "tema",
	"palp", "p03", "fjmp", "ea2", "tbro", "tpip", "ps18", "thp2", "v15", "pjas", "trvr", "ppro", "fmom", "xana", "txln", "slx", "ps14", "t30a", "punh", "f12", "ddd", "mpr", "smid", "pal99", "und", "p30h", "pj21", "l14", "fbro", "ddc", "ajmp", "tori", "tafr", "paer", "wmc", "tmic", "f11", "tdom", "tafc", "svow", "gnt", "tarb", "wdmu", "tcma", "ddo", "mgb", "p06", "dkm", "ea1", "ps17", "pncc", "oe01", "p23", "rqs", "phel", "p11", "tdka", "tlcc", "oc14", "p5dn", "p09", "pm15", "tisd", "pogw", "g09", "tnec", "tiko", "tm13", "twoe", "pfrf", "pbok", "cc2", "pmps08", "tm10", "tmid", "tfth", "pcmd", "tust", "pcon", "ss3", "pxtc", "f03", "f10", "s00", "togw", "tone", "dd2",
	"cp1", "pnph", "pal01", "plg21", "f09", "f04", "evg", "troe", "ocm1", "pelp", "tdmu", "twar", "tima", "t2x2", "sch", "wmom", "p30m", "pf23", "teld", "ptkdf", "past", "g11", "tdmc", "pm13", "pwwk", "f14", "pcmp", "yneo", "psus", "p08", "tddt", "psdc", "mkhm", "phpr", "tgtc", "pmps11", "fone", "tc19", "p2hg", "tltr", "g18", "pl22", "pw21", "tths", "tsom", "pnat", "p04", "p30t", "ylci", "fclu", "bot",
	"tzen", "parl", "pdgm", "g10", "tstx", "g05", "p10", "pgpx", "pw23", "papc", "thou", "mone", "f02", "v13", "tgk1", "j16", "p8ed", "q06", "v09", "l15", "tthb", "taer", "tbth", "tdtk", "fnm", "pmps06", "tgk2", "ha1", "mznr", "tgvl", "pal05", "v14", "ss2", "tevg", "trex", "purl", "pths", "tcns", "oc13", "mmh2", "sneo", "psok", "v17", "pw11", "p22", "thp3", "tm11", "v12", "tm15", "f01", "ptdmu", "tddc", "mdmu", "ppp1", "prw2", "j17", "tugl", "tbrc", "pons", "plgm", "gdy", "pmps10", "ptbro", "ps19", "tala", "g01", "wone", "pdp15", "tmul", "g07", "tmbs", "mafr", "p10e", "f18", "h17", "phj", "pw12", "sznr", "tfrf", "pm10", "pjud", "pss4", "wwoe", "g03", "cp2", "pm12",
	"f15", "g00", "j18", "pdka", "pbng", "pisd", "pl24", "pjse", "hho", "parb", "j19", "pss2", "pptk", "tcn2", "pdp13", "oc21", "puds", "ptsp", "pdp14", "pbook", "mmid", "g08", "peve", "te01", "tm12", "cc1", "ph21", "pmor", "pr2", "ph17", "pavr", "p05", "l13", "tgn2", "ps16", "g02", "pgru", "pulg", "tavr", "tdvd", "p9ed", "tnph", "pcsp", "oc15", "tbot", "pdis", "v16", "g04", "ph20", "pdp10", "tddg", "tkld", "l16", "thp1", "tddu", "tddh", "plgn", "oc18", "pmps07", "mbro", "ph18", "tdde", "tvoc", "ptg", "oc16", "g99", "trix", "phop", "tddk", "phtr", "tjou", "ptmp", "pmh1", "pnem", "mvow", "tdgm", "pewk", "tbbd", "pmps09", "tund", "pzen", "oc17", "oafc", "oc19", "tdds", "tbng", "prcq", "t10e", "tddl", "plrw", "jgp", "tddd", "proe", "pss1", "psth", "plg20", "pwor", "pm11", "pexo", "pmda", "ptor", "pdrc", "smom", "pal02", "pgpt", "ptsnc", "pmbs", "pf24", "tddi", "pmmq", "pody", "ptsr", "mclb", "pfut", "omic", "pmat", "j15", "pred", "plg22", "tddm", "pscg", "ppls", "pl21", "msnc", "psom", "tjvc", "pshm", "pusg", "pr23", "q07", "pdtp", "prav", "pwos", "pcns", "ppc1", "pmrd", "pala", "pust", "tddf", "slci", "pinv", "pmic", "pdst", "l17", "tcon", "tdd2", "pchk", "ovoc", "ppcy", "plny", "sbro",
}

func contains(s []string, e string) bool {
	for _, a := range s {
		if a == e {
			return true
		}
	}
	return false
}
