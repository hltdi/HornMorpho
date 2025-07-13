# Amharic ambiguity categories

## Features

1. Noun or adjective possessive suffixes vs. definite determiners (articles)

	The noun suffixes -ኡ and -ዋ are usually ambiguous; they can either function as possessives (= English 'his' or 'her') or as definite articles (= English 'the'). Sometimes they are genuinely ambiguous, that is, impossible to disambiguate (except probabilistically) given only one sentence.
   
   The suffix can also appear on an adjective modifying a noun or an adjective functioning as a noun.
  
   * -ኡ
   	
   			እናቱ ናፈቀችው ።  
   			Gender[psor]=Masc|Number[psor]=Sing|Person[psor]=3
   		
   			ፕሬዚዴንቱ ንግግር አደረጉ ።  
   			Definite=Def|Gender=Masc
   			
   			ትልቁን መረጥኩ ።
   			Definite=Def|Gender=Masc
   			
   			[ambiguous]   
   			በቱን ተከራየ ። 
   			
   * -ዋ

   			ባሏ ናፈቃት ።  
   			Gender[psor]=Fem|Number[psor]=Sing|Person[psor]=3
   			
   			[possibly ambiguous]
   			አይጧ ጠፋች ።  
   			Definite=Def|Gender=Fem
   			
   			[ambiguous]
   			ድመቷ ጠፋች ።
   			

2. Relative verbs with object suffixes vs. definite determiners (articles)

	This corresponds to 1. for suffixes on relative verbs that modify nouns or function as nouns, except that in this case the interpretation other than the definite article is as an object.
There is only ambiguity between the masculine article and 3rd person singular masculine object. The suffix has the form -ው, -ኧው, or -ት, depending on the verb stem.
In disamguation, it can help to see if the translation in English has an object pronoun, *him* or *it*.

	The easiest cases are with intransitive verbs like ሄደ because they can't take objects. (HM does not currently know which verbs are intrnansitive, so the suffix still needs to be disambiguated.)
	
		መቼ ነው ይምትሄደው ?
		Definite=Def
		
	Note that the most natural translation in English may not include the article *the*: 'when is that you're going?' But we can see how the suffix makes the reference definite by rephrasing it: 'when is the time that you're going?'
		
	In other cases the suffix clearly corresponds to *him* or *it* in English.
	
		የሚከሱት ሰዎች አይተውት አያውቁም ።
		'(the) people who are accusing _him_ have never seen him'
		Gender[obj]=Masc|Number[obj]=Sing|Person[obj]=3
		
	Other cases are harder and may be genuinely ambiguous.
	
		ልጁ የሸጠው መጽሐፍ ትልቅ ነው ።
		
	I suggest we use the definite article (Definite=Def) for these cases.	
3. Verb active vs. passive voice
4. 3sf vs. 2sm

## POS

1. N vs. ADJ
2. ADP vs. SCONJ: 
ስለሚሉት ጉዳዮች ማወቅ አለባቸው ።
3. DET vs. PRON
4. ADV vs. INTJ
5. ADV vs. CCONJ
6. N vs. PROPN

## Lemma

1. አለ, አለኝ, አላቸው, etc.
2. ነበረ
