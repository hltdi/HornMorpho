## Abbreviations
# maximal forms
{በላ}: a=0,v=0;		a=0,v=p;	a=0,v=a;	a=0,v=as;	a=a,v=p;	a=a,v=a;	a=i,v=0;	a=i,v=p;	a=i,v=a
{ሰበረ}: a=0,v=0;	a=0,v=p;	a=0,v=as;	a=a,v=p;	a=a,v=a;	a=i,v=0;	a=i,v=p;	a=i,v=a
#          S=1,O=o	S=1,O=0 	S=1,O=oi	S=1,O=0	S=1,O=o	S=1,O=0?	S=1,v=0	S=1,O=o
# ditransitive verbs like ሰጠ have different v/v features
{ዘነበ}: a=0,v=0;	a=0,v=as ; a=i,d=m
#          S=0,O=0	S=1,O=0
{ሮጠ}: a=0,v=0;		a=0,v=p;	a=0,v=a;	a=0,v=as;	a=a,v=p;	a=a,v=a;	a=i,v=0;	a=i,v=p;	a=i,v=a
#          S=1,O=0     	S=0,O=0	S=1,O=o	S=1,O=oi	S=1,O=0	S=1,O=o	S=1,O=0?	S=1,v=0	S=1,O=o
# 2=እ: no a=a
{ሳመ}: a=0,v=0;		a=0,v=p;	a=0,v=as;	a=i,v=0;	a=i,v=p;	a=i,v=a
{ነገረ}: a=0,v=0;		a=0,v=p;	a=0,v=as;	a=a,v=p;	a=a,v=a;	a=i,v=0;	a=i,v=p;	a=i,v=a
{አለቀሰ}: a=0,v=p;	a=0,v=a;	a=0,v=as;	a=a,v=p;	a=a,v=a;	a=i,v=0;	a=i,v=p;	a=i,v=a
# 1=እ; no a=a; a=i,v=as
{አመመ}:	a=0,v=0;	a=0,v=p;	a=0,v=as;	a=i,v=0;	a=i,v=p;	a=i,v=a;	a=i,v=as
{ደከመ}:	a=0,v=0;	a=0,v=p;	a=0,v=a;	a=a,v=p;	a=a,v=a
{አደረገ}:	a=0,v=a;	a=0,v=p;	a=0,v=as;	a=a,v=p;	a=a,v=a;	a=i,v=p;	a=i,v=a
{ተቀመጠ}: a=0,v=p;	a=0,v=as;	a=i,v=p;	a=i,v=a
# also transitive ተረከበ ተገነዘበ
{ተመለከተ}: a=0,v=p;	a=0,v=a;	a=i,v=p;	a=i,v=a
{ተዳደረ}:	a=i,v=p;	a=i,v=a;	a=i,v=as

<እ ው ቅ>		c=A
  a=0,v=0 ; a=0,v=p ; a=0,v=as ; a=0,v=ast ; a=i,v=0 ; a=i,v=p ; a=i,v=ast

<ን እ ቅ>	     c=A
  a=0,v=0 ; a=0,v=p ; a=0,v=as ; a=i,v=0 ; a=i,v=p ; a=i,v=a ; a=i,v=ast

<ን ብ ር>	     c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=ast ; a=i,v=a ; a=i,v=ast ; a=i,d=m

# ማረ: forgive, sense 1
<ም እ ር>	     c=A,s=1
  a=0,v=0 ; a=0,v=p ; a=0,v=as ; a=i,v=p ; a=i,v=a ; a=i,d=m

# ተማረ: learn, sense 2
<ም እ ር>	     c=A,s=2
  a=0,v=p ; a=0,v=ast ; a=i,d=m

# አረጀ: be old, sense 1
<ር ጅ ይ>	    c=A,s=1
  a=0,v=a ; a=0,v=as ; a=i,v=p ; a=i,d=m

# አ/ራጀ: give a little, sense 2
<ር ጅ ይ>	    c=A,s=2
  a=a,v=a ; a=i,d=m

# ፈራ: fear, sense 1
<ፍ ር እ>	    c=A,s=1
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=p ; a=a,v=a ; a=i,v=0 ; a=i,v=a ; a=i,v=as ; a=i,v=p

# ተፈራ: be produced, sense 2
<ፍ ር እ>	  c=A,s=2
  a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m

<ም ጥ እ>		c=A
  # restrict a=0,v=0 so that irregular ና/ነይ/ኑ is used for t=j,sp=2,-neg
  a=0,v=0,t=p|c|i|0;a=0,v=0,t=j,sp=1|3;a=0,v=0,t=j,sp=2,+neg;a=0,v=p;a=0,v=a;a=0,v=as;a=a,v=p;a=a,v=a;a=i,v=0;a=i,v=p;a=i,v=a

<ግ ኝ ይ>		c=A
  # restrict regular forms to a=0|a so irregular ተገኛኘ can be handled specially
  a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p

<ጽ ል ይ>	      c=B,+strong
  a=0,v=0 ; a=a,v=a ; a=a,v=a ; a=i,d=m

<እ ይ ይ>	     c=A,-dup23,tmp=[2=X,3=ይ]
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=0,v=ast ; a=i,v=0 ; a=i,v=ast ; a=i,v=p

<ት ግ ል>	      c=C
  a=0,v=0 ; a=0,v=as ; a=a,v=a ; a=i,v=0

<እ ክ ል>	     c=A
  a=0,v=0 ; a=0,v=p ; a=0,v=ast ; a=i,v=0 ; a=i,v=ast ; a=i,v=p

<እ ክ ል>	  c=B
  a=0,v=0 ; a=0,v=p ; a=0,v=as ; a=i,v=p ; a=i,d=m

<ል ም ድ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=as ; a=i,v=p
<ን ግ ድ>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=ast ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ግ ብ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=as ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ል ቅ ም>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ል ቅ ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ም ር እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ም ት እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ም ው ት>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ር ት እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ር ው ጥ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ር ድ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ር ግ ም>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ር ፍ ድ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=as ; a=i,v=p
<ስ ር ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ስ ፍ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ቅ ብ እ>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ቅ ው ም>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ብ ል እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ብ ል ጥ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ን ስ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ን ብ ብ>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ን ዝ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ኩ ር ፍ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ክ ፍ ል>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ክ ፍ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ው ር እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ው ር ድ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ው ቅ ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ው ጥ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ድ ግ ም>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ጥ ል እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጥ ር እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ጥ ይ ቅ>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ፍ ት እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ል ም ን>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ል ም ጥ ጥ>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ል ብ ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ል ክ እ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ል ጉ ድ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ል ጥ ፍ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ሙ ል እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ሙ ግ ድ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ሙ ጭ ር>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ም ል ክ ት>	c=E
  a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ም ስ ል>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ም ው ቅ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=as ; a=i,v=p
<ር ስ እ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ር ግ ጥ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ር ግ ፍ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ር ጭ ይ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ስ ል ች ይ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ስ ር ቅ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ስ ር እ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ስ ቅ ቅ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ስ ን ብ ት>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ስ ድ ብ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ስ ፍ ር>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ቁ ር ጥ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ቁ ፍ ር>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ቅ ብ ር>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ቅ ን ዝ ር>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ቅ ድ እ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ቅ ጥ ር>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ቅ ጥ እ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ብ ቅ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ብ ጅ ይ>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ን ቅ ል>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ን ቅ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ን ብ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ን ድ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ን ጥ ር>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ን ጥ ቅ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ን ፍ ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ን ፍ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ኩ ን ን>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ክ ብ ብ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ክ ድ እ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ክ ጅ ል>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ው ል ቅ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ው ሽ ም>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ው ቅ ስ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ዝ ን እ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ዝ ው ር>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ዝ ግ ም>	c=A
  a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ዝ ግ እ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ድ ል እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ድ ም ር>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ድ ም ጥ>	c=A
  a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ድ ር ቅ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ድ ን ብ ር>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ድ ው ል>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ድ ፍ ር>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ድ ፍ እ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ግ ል ብ ጥ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ግ ም እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ግ ዝ እ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጥ ም ር>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጥ ቅ ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ጥ ብ ቅ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጥ ግ እ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጭ ር ስ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ፉ ክ ር>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ፍ ል ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ፍ ር ድ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ፍ ቅ ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ል ም ጥ>	c=B
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ል ስ ስ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ል ቅ ል ቅ>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ል ቅ ቅ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ል እ ጥ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ል ይ ይ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ሙ ክ ር>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ም ል ጥ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ም ር ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ም ር ር>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ም ር ቅ>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ም ክ ር>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ም ክ ት>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ም ዝ ን>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ም ጥ ን>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ም ጥ ጥ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ር ቅ ቅ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ር ብ ሽ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ር ብ ብ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ር እ ቅ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ር ክ ብ>	c=A
  a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ር ዝ ም>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ስ ል እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ስ ል ጥ ን>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ስ ም ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ስ ን ክ ል>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ስ ክ ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ሽ ት ት>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ቁ ል እ>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ቁ ል ፍ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ቁ ን ጅ ይ>	c=E
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ቁ ጭ ይ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a
<ቅ ል እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ቅ ል ድ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ቅ ም ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ቅ ር ብ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ቅ ን ስ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ቅ ን እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ቅ እ ም>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ቅ ድ ድ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ቅ ጥ ል>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ቡ ጭ ቅ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ብ ር ት እ>	c=E
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ብ ት ን>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ብ ድ ር>	c=B
  a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ት ር ክ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ት ን ት ን>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ት ኩ ስ>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ን ክ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ን ግ ር>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ን ግ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ን ጥ ል>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ን ጥ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<እ ም ን>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=ast ; a=i,v=p
<እ ስ ብ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=ast ; a=i,v=p
<እ ሽ ይ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=ast ; a=i,v=p
<እ ቅ ፍ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<እ ዝ ብ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=ast ; a=0,v=p ; a=i,d=m ; a=i,v=ast ; a=i,v=p
<ኩ እ ል>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ክ ል ል>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ክ ል ስ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ክ ር ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ክ ስ ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ክ ብ ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ው ስ ን>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ው እ ል>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=ast ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ው እ ጥ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ው ክ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ው ግ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ዝ ል ል>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ዝ ል ቅ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ዝ ም ት>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ዝ ን ግ እ>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ይ እ ዝ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ድ ቁ ስ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ድ ብ ል ቅ>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ድ ን ቅ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጉ ር እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ግ ር እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ግ ት ር>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ግ እ ጥ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ግ ድ ድ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ግ ጥ ም>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ግ ፍ እ>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ጥ ል ል>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጥ ም እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ጥ ር ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጥ ር ቅ ም>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጥ ቁ ም>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ጥ ቅ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጥ ብ ብ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ጥ ን እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጥ ፍ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጭ ው ህ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ፍ ል እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ፍ ር ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ፍ ት ግ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ፍ ን ክ ት>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ፍ ጅ ይ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ል ብ ቅ>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ል እ ክ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ል ው ጥ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ል ግ ም>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ል ግ ጥ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ል ፍ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ሙ ል ጭ>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ሙ ግ ስ>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ም ል ስ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ም ር ም ር>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ም ር ት>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ም ር ን>	c=B
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ም ር ጥ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ም ስ ክ ር>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ም ስ ግ ን>	c=E
  a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ም ሽ ይ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ም ን ቅ ር>	c=E
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ም ን ች ክ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ም ን ጭ ቅ>	c=E
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ም እ ል>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ም ዝ ዝ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ም ግ ም ግ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ር ክ ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ር ግ ብ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ስ ል ፍ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ስ ም እ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ስ ቅ ል>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ስ ብ ስ ብ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ስ ብ እ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ስ ን ዝ ር>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ስ ን ጥ ቅ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ስ እ ም>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ስ እ ቅ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ስ እ ብ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ስ እ ት>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ስ ው እ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ስ ድ ድ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ስ ጥ እ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ስ ጥ ይ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ሽ ል ም>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ሽ ም ግ ል>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ሽ ሽ ይ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ሽ ኝ ይ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ሽ ክ እ>	c=A
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ሽ ው ም>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ቁ ር ስ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ቁ ር እ>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ቁ ስ ል>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ቁ ጥ ር>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ቅ ል ል>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ቅ ም ቅ ም>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ቅ ም እ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ቅ ር ጽ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ቅ ር ፍ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ቅ ን ቅ ን>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ቅ ን ብ ር>	c=E
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ቅ ን ት>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ቅ ይ ም>	c=B
  a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ቅ ይ ር>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ቅ ድ ም>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ቅ ፍ ፍ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ብ ር ክ ት>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ብ ር ድ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ብ ስ እ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ብ እ ት>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ብ ድ ል>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ብ ጥ ር>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ብ ጥ ስ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ብ ጥ ብ ጥ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ብ ጥ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ት ር ጉ ም>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ት ች ይ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ት ፍ እ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ች እ ል>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ች ኩ ል>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ኩ ት>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ን ው ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ን ው ጥ>	c=B
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ን ጥ ብ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ጽ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ፍ ቅ>	c=C
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<እ ል ቅ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=ast ; a=i,v=p
<እ ል ፍ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=ast ; a=i,v=p
<እ ም እ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<እ ር ቅ>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<እ ስ ር>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=ast ; a=i,v=p
<እ ስ ስ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<እ ን ቅ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<እ ዝ ን>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=ast ; a=i,v=p
<እ ድ ግ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<እ ጉ ል>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ኩ ር እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ክ ል ክ ል>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ክ ስ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ክ ስ ክ ስ>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ክ እ ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ክ እ ድ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ክ ፍ ፍ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ው ር ር>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ው ር ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ው ር ው ር>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ው ስ እ>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ው ቅ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ው ን ብ ድ>	c=E
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ው ን ጅ ል>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ው እ ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ው ድ ስ>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ው ድ ቅ>	c=A
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ው ጅ ይ>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ው ግ ድ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ዝ ር ግ እ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ዝ ር ፍ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ዝ ብ ር ቅ>	c=F
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ዝ ብ ት>	c=B
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ዝ ው ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ዝ ፍ ን>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ ል ብ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ ም ም>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ ም ጥ>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ድ ር ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ ቅ እ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ ብ ብ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ ብ ድ ብ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ ን ስ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ እ ር>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ድ እ ን>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ድ ክ ም>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ ው ል>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ድ ግ ን>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ድ ግ ፍ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ድ ፍ ቅ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጅ ም ር>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጉ ል እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጉ ስ ቁ ል>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጉ ስ ጉ ስ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጉ ት ት>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጉ እ ዝ>	c=A
  a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጉ ድ ል>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ግ ል ል>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ግ ም ት>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ግ ም ግ ም>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ግ ር ፍ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ግ ስ ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ግ ብ ዝ>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ግ ት እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ግ ን ብ እ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ግ ን ጥ ል>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ግ ን ፍ ል>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ግ ድ ል>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ግ ጭ ይ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጥ ል ፍ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ጥ ም ድ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጥ ር ጥ ር>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጥ ብ ጥ ብ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጥ ን ቅ ቅ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጥ እ ል>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጥ እ ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጥ ይ ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጥ ግ ብ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጥ ግ ን>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ጥ ጥ ር>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጥ ጥ እ>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጭ ብ ጥ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጭ ን ቅ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጭ እ ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ጭ እ ን>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጭ ክ ን>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጭ ፍ ር>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጭ ፍ ጭ ፍ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጽ ን እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ጽ ድ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ፍ ል ግ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ፍ ር ም>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ፍ ስ ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ፍ ቅ ድ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ፍ ት ሽ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ፍ ን ጥ ር>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ፍ ን ጥ ቅ>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ፍ ግ ፍ ግ>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ፍ ጭ ይ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ፍ ጽ ም>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ል ም ስ ስ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ል ም እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ል ስ ል ስ>	c=E
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ል ስ ን>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ል ብ ድ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ል ት ም>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ል እ ግ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ል ው ስ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ል ዝ ብ>	c=B
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ል ፍ ል ፍ>	c=E
  a=0,v=0 ; a=0,v=as ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ሙ ሽ ል ቅ>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ሙ ጭ ይ>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ም ር ዝ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ም ር ግ>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ም ስ ቅ ል>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ም ስ ግ>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ም ሽ ት>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=i ; a=0,v=p ; a=i,d=m
<ም ት ር>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ም ች ይ>	c=B
  a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ም ን ም ን>	c=E
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ም ን ት እ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ም ኝ ይ>	c=A
  a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ም እ ጥ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,v=0
<ም ክ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,v=0
<ም ድ ብ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ም ግ ብ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ር ም ድ>	c=C
  a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ር ቁ ት>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ር ብ ር ብ>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ር ብ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ር ክ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ር ግ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ር ግ ድ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ስ ል ም>	c=A
  a=0,v=0 ; a=0,v=as ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ስ ል ስ ል>	c=E
  a=0,v=0 ; a=0,v=as ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ስ ል ቅ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ስ ር ግ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ስ ር ጭ ይ>	c=F
  a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ስ ብ ር>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ስ ብ ቅ>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ስ ብ ብ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ስ ብ ጥ ር>	c=F
  a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ስ ት ር>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ስ ን ድ እ>	c=F
  a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ስ እ ስ እ>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ስ ክ እ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ስ ይ ም>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ስ ግ ድ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ስ ፍ ን ጥ ር>	c=G
  a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ስ ፍ ፍ>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ሹ ክ ሹ ክ>	c=E
  a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ሽ ል ት>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ሽ ም ቅ ቅ>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ሽ ር ሽ ር>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ሽ ር ክ ት>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ሽ ር ፍ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ሽ ቅ ል>	c=B
  a=0,v=0 ; a=0,v=as ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ሽ ቅ ብ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ሽ ን እ>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ሽ ን ፍ>	c=A
  a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ሽ እ ል>	c=A
  a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ሽ ክ ም>	c=B
  a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ሽ ግ ር>	c=C
  a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ሽ ፍ ን>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ቁ ል ል>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ቁ ር ቁ ዝ>	c=E
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ቁ ሽ ሽ>	c=B
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ቁ ን ጥ ጥ>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ቁ ጭ ይ>	c=C
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=a,v=a ; a=i,d=m
<ቅ ል ጥ ም>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ቅ ም ም>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ቅ ር ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ቅ ር ይ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ቅ ር ጥ ፍ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ቅ ር ጥ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ቅ ስ ቅ ስ>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ቅ ስ ት>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ቅ ብ ል>	c=B
  a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ቅ ን ጭ ብ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ቅ እ ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ቅ ዝ ቅ ዝ>	c=E
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ቅ ይ ድ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ቅ ይ ጥ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ቅ ጥ ቅ ጥ>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ቡ ጭ ር>	c=C
  a=0,v=0 ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ብ ል ሽ ይ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ብ ል ቅ ጥ>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ብ ል ት>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ብ ር ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ብ ር ቅ ስ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ብ ር እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ብ ር ግ ድ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ብ ስ ብ ስ>	c=E
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ብ ሽ ቅ ጥ>	c=E
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ብ ሽ ቅ>	c=B
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ብ ቅ ል>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ብ እ ል>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ብ እ ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ብ ክ ል>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ብ ክ ን>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ብ ዝ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ብ ይ ን>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ት ል ም>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ት ር ም ስ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ት ር ት ር>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ት ር ፍ>	  c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,v=a ; a=i,v=0
<ት ን ኩ ስ>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ት ክ ል>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ት ክ እ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ች ይ ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ን ሹ ክ ሹ ክ>	c=G
  a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ሽ ር ሽ ር>	c=G
  a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ቁ ር>	c=A
  a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ቅ ል ቅ ል>	c=G
  a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ቅ ር ፍ ፍ>	c=G
  a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ቅ ብ ድ ድ>	c=G
  a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ቅ ን ቅ>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ቅ ፍ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ን ቡ ር ቅ ቅ>	c=G
  a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ብ ብ>	c=A
  a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ክ ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ን ክ ት ክ ት>	c=G
  a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ው ር>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ን ዝ ር ጥ ጥ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ን ዝ ር ፍ ጥ>	c=G
  a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ዝ ን ዝ>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ድ ር ድ ር>	c=G
  a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ድ ድ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ድ ፍ>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ን ጉ ድ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ግ ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ግ ድ ግ ድ>	c=G
  a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ጥ ል ጥ ል>	c=G
  a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ጥ ብ ጥ ብ>	c=G
  a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ጭ ር ጭ ር>	c=G
  a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ጭ ይ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ን ፍ ር ጥ ጥ>	c=G
  a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ፍ ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ፍ ን ፍ>	c=E
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<እ ር ስ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=ast
<እ ር እ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=p
<እ ር ድ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=p
<እ ብ ል>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,v=0 ; a=i,v=ast ; a=i,v=p
<እ ብ ር>	c=A
  a=0,v=0 ; a=0,v=as ; a=i,d=m ; a=i,v=ast ; a=i,v=p
<እ ት ም>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=p
<እ ን ክ ስ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=p
<እ ክ ክ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,v=0
<እ ድ ር>	c=A
  a=0,v=0 ; a=0,v=as ; a=i,d=m ; a=i,v=ast ; a=i,v=p
<እ ጥ ቅ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=p
<እ ጥ ብ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,v=0 ; a=i,v=p
<እ ጥ እ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=p
<እ ጭ ይ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=p
<እ ፍ ር>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=p
<እ ፍ ን>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=p
<ኩ ም ት ር>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ኩ ር ት ም>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ኩ ር ጅ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ኩ ስ ስ>	c=B
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ኩ ስ ኩ ስ>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ኩ ት ኩ ት>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ክ ም ች ይ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ክ ብ ት>	c=B
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ክ ብ ድ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ክ ት ል>	c=B
  a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ክ ት ት>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ክ ት ክ ት>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ክ ን ን>	c=B
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ክ እ ብ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ክ ክ እ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ክ ፍ ት>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ው ል ድ>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ው ል ግ ድ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ው ቅ ጥ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ው ን ጭ ፍ>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ው ክ ብ>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ው ዝ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ው ዝ ው ዝ>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ው ይ ይ>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ው ድ ድ>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ው ጥ ር>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ው ጥ ን>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ዝ ል ፍ>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ዝ ር ር>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ዝ ር እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ዝ ር ክ ት>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ዝ ብ ጥ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ዝ ን ቅ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ዝ ን ጥ ል>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ዝ ን ፍ>	c=C
  a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ዝ እ ት>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ዝ ግ ብ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ዝ ግ ጅ ይ>	c=F
  a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ዝ ፍ ቅ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ ል ህ>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ ል ል>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ድ ል ድ ል>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ ም ቅ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ ም እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ ር ብ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ድ ር ት>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ድ ር እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ ር ድ ር>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ ር ግ>	c=A
  a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ድ ር ግ>	c=C
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ድ ቅ ቅ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ድ ብ ል>	c=B
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ ብ ቅ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ድ ን ቁ ር>	c=E
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ ን ቅ ፍ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ድ ን ግ ር>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ድ ን ግ ጥ>	c=E
  a=0,v=0 ; a=0,v=as ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ ፍ ን>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ድ ፍ ድ ፍ>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ጅ ቡ ን>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጅ ይ ል>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጉ ል ም ስ>	c=E
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጉ ም ዝ ዝ>	c=E
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጉ ር ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጉ ድ እ>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ጉ ጥ ጥ>	c=B
  a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ግ ል ም ጥ>	c=F
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ግ ል ጽ>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ግ ም ስ>	c=A
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ግ ም ድ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ግ ር ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ግ ን ን>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ግ ን ዝ ብ>	c=E
  a=0,v=as ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ግ እ ል>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ግ እ ም>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ግ እ ዝ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ግ ይ ይ>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ግ ይ ጥ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ግ ድ ም>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ግ ጥ ብ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0 ; a=i,v=p
<ግ ፍ ት ር>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ጥ ል ቅ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጥ ም ቅ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ጥ ም ዝ ዝ>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጥ ር ስ>	c=B
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጥ ር ግ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ጥ ቁ ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ጥ ቅ ል ል>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጥ ቅ ም>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጥ ብ ቅ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጥ ብ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ጥ ን ቁ ል>	c=E
  a=0,v=0 ; a=0,v=as ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጥ ን ክ ር>	c=E
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጥ ን ጥ ን>	c=E
  a=0,v=a ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጥ እ ም>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ጥ እ ፍ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጥ ይ ፍ>	c=B
  a=0,v=as ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጥ ፍ ፍ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጭ ም ል ቅ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጭ ም ር>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጭ ም ት ር>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጭ ር ፍ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጭ ቅ ጭ ቅ>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጭ ብ ጭ ብ>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ጭ ን ግ ፍ>	c=E
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጭ ው ት>	c=C
  a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጽ እ ፍ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ፍ ት ን>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ፍ ን ቅ ል>	c=E
  a=0,v=0 ; a=0,v=p ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ፍ ን ን>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ፍ ን ጭ ይ>	c=E
  a=0,v=0 ; a=0,v=as ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ፍ እ ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ፍ እ ቅ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ፍ ዝ ዝ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ፍ ይ ዝ>	c=A
  a=0,v=a ; a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ፍ ጥ ጥ>	c=A
  a=0,v=0 ; a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ሁ ም ጥ ጥ>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m
<ል ም ል ም>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ል እ ም>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ል እ ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ል እ ቅ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,v=0
<ል እ ብ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ል እ ፍ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ል ክ ክ>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ል ጉ ም>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ል ግ እ>	c=B
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ል ጥ ል ጥ>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ል ጥ ቅ>	c=B
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ል ጭ ይ>	c=C
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ሙ ል ል>	c=B
  a=0,v=0 ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ሙ ል ፍ ጥ>	c=E
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ሙ ኝ ይ>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ሙ ግ ት>	c=B
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ሙ ጥ ጥ>	c=C
  a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ሙ ጭ ር>	c=C
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ም ል ል>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ም ል ል>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ም ል ም ል>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ም ል ክ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ም ል ድ>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ም ር ክ>	c=C
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ም ስ ን>	c=B
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ም ን ን>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ም ን ዝ ር>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,v=0
<ም ን ጥ ር>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0
<ም እ ስ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0
<ም ዝ ብ ር>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ም ዝ ግ ብ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ም ድ ድ>	c=B
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ር ሽ ን>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ር እ ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ር እ ብ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ር እ ድ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ር ግ ዝ>	c=A
  a=0,v=a ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ስ ል ስ>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m
<ስ ም ም>	c=B
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ስ ም ር እ>	c=F
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ስ ር ዝ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0
<ስ ቅ ይ ይ>	c=F
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ስ እ ል>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ስ ይ ር>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ስ ግ እ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ስ ጥ ም>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ስ ፍ ን>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m
<ሹ ል ክ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ሽ ም ት>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ሽ ም እ>	c=C
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ሽ ር ክ>	c=C
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ሽ ቅ ል>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ሽ ቅ ጥ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ሽ ብ ር>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ሽ ብ ሽ ብ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ሽ እ ር>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ሽ ኩ ት>	c=B
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ሽ ክ ር>	c=C
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ሽ ው ል>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m
<ሽ ው ፍ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ሽ ይ ት>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ሽ ይ ጥ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0
<ሽ ፍ ት>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ቁ ል ቁ ል>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m
<ቁ ር ም ድ>	c=E
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ቁ ር ቁ ስ>	c=E
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ቁ ር ኝ ይ>	c=F
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ቁ ር ጥ ም>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0
<ቁ ይ ይ>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m
<ቁ ጥ ር>	c=C
  a=0,v=0 ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ቁ ጥ ቁ ጥ>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m
<ቅ ል ም>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ቅ ል ስ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0
<ቅ ል ቅ ል>	c=F
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ቅ ል ው ጥ>	c=F
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0
<ቅ ል ጥ ፍ>	c=E
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ቅ ል ጥ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ቅ ር ቅ ር>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ቅ ን ጥ እ>	c=F
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ቅ ኝ ይ>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ቅ ኝ ይ>	c=C
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ቅ እ ጥ እ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ቅ ው ስ>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ቅ ይ ስ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ቅ ድ ስ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ቅ ድ ጅ ይ>	c=F
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ቅ ጭ ቅ ጭ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ቡ ር ቡ ር>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ቡ ክ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ብ ር ቅ>	c=B
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ብ ስ ል>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ብ ስ ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ብ ስ ጭ ይ>	c=F
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ብ እ ብ እ>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m
<ብ ዝ ብ ዝ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ብ ዝ ት>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ብ ድ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,v=0
<ት ል ል>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ት ም ም>	c=B
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ት ም ት ም>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m
<ት ም ን>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ት ር ት>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ት ብ እ>	c=A
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ት ት ር>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ት ን ን>	c=B
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ት ን ፍ ስ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0
<ት ግ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m
<ች ግ ር>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ን ት ር ክ>	c=E
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን እ ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ን እ ድ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ክ ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ክ ብ ክ ብ>	c=G
  a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ው ዝ>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ዝ ዝ>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ድ ል>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,v=0
<ን ጉ ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ጉ ት>	c=A
  a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ጉ ድ ጉ ድ>	c=G
  a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ጥ ፍ>	c=A
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ጭ እ>	c=A
  a=0,v=0 ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ን ፍ ር ቅ>	c=E
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ን ፍ ግ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<እ ል ም>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<እ ም ም>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0
<እ ር ም>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=p
<እ ር ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m
<እ ር ግ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<እ ሽ ግ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<እ ብ ስ>	c=A
  a=0,v=0 ; a=0,v=as ; a=i,d=m ; a=i,v=p
<እ ብ ይ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<እ ብ ጥ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0
<እ ን ስ>	c=A
  a=0,v=0 ; a=0,v=as ; a=i,d=m ; a=i,v=p
<እ ን ጥ ፍ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<እ ክ ም>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<እ ክ ት>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<እ ው ር>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<እ ው ክ>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<እ ው ጅ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<እ ዝ ዝ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<እ ድ ል>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0
<እ ድ ም>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<እ ድ ስ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0
<እ ድ ን>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<እ ጅ ብ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<እ ግ ል>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0
<እ ግ ዝ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=p
<እ ጥ ር>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<እ ፍ ስ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<እ ፍ ግ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m ; a=i,v=p
<ኩ ል ሽ ይ>	c=F
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ኩ ር ኩ ም>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ኩ ስ ት ር>	c=E
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ኩ ስ እ>	c=A
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ኩ ብ ል ል>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ኩ እ ት>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ክ ል ብ>	c=A
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ክ ም ር>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ክ ር ም>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,v=0
<ክ ር ክ ር>	c=E
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ክ ር ይ ይ>	c=F
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ክ ስ ል>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ክ ስ ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ክ ስ ት>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ክ ሽ ፍ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ክ ት ል ብ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ክ ት ብ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ክ ች ች>	c=B
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ክ ን ብ>	c=A
  a=0,v=0 ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ክ እ ን>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ው ል ም ም>	c=F
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ው ል ው ል>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ው ር ጭ ይ>	c=F
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ው ር ፍ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ው ሽ ይ>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m
<ው ብ ር እ>	c=E
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ው ን ክ ር>	c=E
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ው እ ብ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ው ክ ል>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ው ዝ ት>	c=B
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ው ድ ር>	c=B
  a=0,v=0 ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ው ድ ጅ ይ>	c=F
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ዝ ም ር>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ዝ ቅ ዝ ቅ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ዝ ብ እ>	c=A
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ዝ ን ብ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m
<ዝ ን ን>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m
<ዝ ክ ር>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ዝ ው ት ር>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ዝ ይ ም>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ዝ ይ ር>	c=B
  a=0,v=0 ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ድ ል ቅ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ድ ር ጅ ይ>	c=E
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ ስ ስ>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ድ ቅ ል>	c=B
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ ብ ር>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ድ ብ ስ>	c=C
  a=0,v=0 ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ድ ብ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ድ ን ብ ዝ>	c=E
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ድ ን ን>	c=B
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,v=0
<ድ ኝ ይ>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ድ እ ጥ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ድ ጉ ም>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ድ ግ ስ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ድ ግ ድ ግ>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m
<ድ ፍ ር ስ>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m
<ጅ ግ ን>	c=A
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጉ ል ብ ት>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ጉ ል ት>	c=B
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ጉ ም ድ>	c=A
  a=0,v=0 ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጉ ር ም ም>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ጉ ብ ኝ ይ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ጉ ን ጉ ን>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ጉ ን ጭ ይ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ግ ል ብ>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m
<ግ ል ግ ል>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ግ ል ግ ል>	c=F
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ግ ም ጥ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m
<ግ ር ም>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ግ ር ዝ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ግ ር ጥ እ>	c=E
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ግ ብ ር>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ግ ብ ይ ይ>	c=E
  a=0,v=0 ; a=i,v=0 ; a=i,v=a ; a=i,v=p
<ግ እ ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ግ እ ት>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ግ ዝ ት>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ግ ግ ም>	c=B
  a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ግ ፍ ፍ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ጥ ም ም>	c=A
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጥ ብ ስ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ጥ እ ስ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ጥ ው ል>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ጥ ው ፍ>	c=A
  a=0,v=0 ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጥ ዝ ጥ ዝ>	c=E
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጥ ድ እ>	c=A
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጥ ፍ ጥ ፍ>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ጥ ፍ ጥ>	c=C
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ጭ ም ድ ድ>	c=E
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጭ ም ጭ ም>	c=E
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጭ ቁ ን>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ጭ ን ጉ ል>	c=E
  a=0,v=a ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ጭ ይ ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m
<ጭ ፍ ል ቅ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0
<ጭ ፍ ቅ>	c=B
  a=0,v=0 ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ጽ ድ ቅ>	c=A
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m
<ፉ ር ሽ>	c=A
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ፉ ን ን>	c=B
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ፍ ል ቅ ቅ>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ፍ ል ጥ>	c=A
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,v=0
<ፍ ል ፍ ል>	c=E
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ፍ ር ክ ስ>	c=E
  a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ፍ ር ፍ ር>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=p ; a=i,d=m
<ፍ እ ም>	c=A
  a=0,v=0 ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ፍ እ ፍ እ>	c=E
  a=0,v=0 ; a=0,v=a ; a=0,v=as ; a=i,d=m
<ፍ ይ ድ>	c=B
  a=0,v=0 ; a=0,v=as ; a=0,v=p ; a=i,d=m
<ፍ ጥ ም>	c=B
  a=0,v=p ; a=i,d=m ; a=i,v=a ; a=i,v=p
<ፍ ጥ ን>	c=A
  a=0,v=0 ; a=a,v=a ; a=a,v=p ; a=i,d=m
<ል ም ዝ ግ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ል ሽ ቅ>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ል ሽ ይ>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ል ቁ ጥ>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ል ብ ል ብ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ል ብ ብ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ል ብ ጥ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ል እ ል እ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ል ኩ ስ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ል ክ ስ ክ ስ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ል ክ ፍ ክ ፍ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ል ግ ስ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ል ጥ ጥ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ል ፍ ስ ፍ ስ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ል ፍ ፍ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ሙ ል ቅ ቅ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ሙ ር ት>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ሙ ር ድ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ሙ ሽ ር>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ሙ ሽ ይ>	c=C
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ሙ ቅ ሙ ቅ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ሙ እ ሙ እ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ሙ ክ ት>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ሙ ጅ ር>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ሙ ጭ ል ፍ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ም ር ቅ ዝ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ም ስ ር ት>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ም ስ ጥ ር>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ም ስ ጥ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ም ሽ ግ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ም ቅ ቅ>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ም ት ብ>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ም ን ሽ ን ሽ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ም ን ት ፍ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ም ን ኩ ስ>	c=E
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ም ን ጥ ቅ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ም ን ጭ ይ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ም እ ግ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ም ክ ን>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ም ዝ ም ዝ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ም ዝ ግ ዝ ግ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ም ግ ል>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ም ግ ር>	c=C
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ም ግ ድ>	c=C
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ም ግ ጥ>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ም ጥ ቅ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ም ጥ ው ት>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ም ጭ ም ጭ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ም ጽ ው ት>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ር ም ስ ም ስ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ር ም ጥ ም ጥ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ር ስ ር ስ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ር ብ ት ብ ት>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ር ብ ድ ብ ድ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ር እ ር እ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ር ኩ ት>	c=C
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ር ክ ፍ ክ ፍ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ር ግ ር ግ>	c=E
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ር ግ ብ ግ ብ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ር ጥ ብ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ር ፍ ር ፍ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ሱ ም ሱ ም>	c=E
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ስ ል ል>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,v=0
<ስ ል ም ል ም>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ስ ል ቅ ጥ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ስ ል ብ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,v=0
<ስ ል ት>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ስ ል ክ ል ክ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ስ ል ጥ>	c=B
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ስ ም ጥ>	c=A
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ስ ር ስ ር>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ስ ር ጉ ድ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ስ ቅ ስ ቅ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ስ ቅ ይ ይ>	c=E
  a=a,v=a ; a=a,v=p ; a=i,d=m
<ስ ብ ክ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ስ ት ፍ>	c=C
  a=0,v=as ; a=0,v=p ; a=i,d=m
<ስ ን ቅ ር>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ስ ን ቅ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ስ ን ግ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ስ ን ጥ ር>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,v=0
<ስ ን ፍ>	c=A
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ስ ኝ ይ>	c=A
  a=0,v=as ; a=0,v=p ; a=i,d=m
<ስ እ ግ>	c=A
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ስ ክ ን>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ስ ው ር>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ስ ይ ፍ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ስ ግ ር>	c=A
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ስ ግ ስ ግ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ስ ግ ብ ግ ብ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ስ ግ ግ>	c=B
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ሹ ል ቅ>	c=B
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ሹ ል ክ ል ክ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ሽ ል ል>	c=B
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ሽ ል ቅ ቅ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ሽ ም ቅ>	c=B
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ሽ ም ድ ም ድ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ሽ ር ሙ ጥ>	c=E
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ሽ ር ጥ>	c=B
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ሽ ሽ ግ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ሽ ሽ ጥ>	c=C
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ሽ ቁ ጥ ቁ ጥ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ሽ ቅ ን ጥ ር>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ሽ ቅ ድ ድ ም>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ሽ ብ ል ል>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ሽ ብ ል ብ ል>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ሽ ብ ብ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ሽ ን ሽ ን>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ሽ ን ቁ ር>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ሽ ን ቁ ጥ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ሽ ን ት ር>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,v=0
<ሽ ን ግ ል>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ሽ እ ጥ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ሽ ኩ ር ም ም>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ሽ ክ ር ክ ር>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ሽ ክ ሽ ክ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ሽ ው ቅ>	c=A
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ሽ ጉ ር>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ሽ ጉ ጥ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ሽ ግ ሽ ግ>	c=F
  a=0,v=as ; a=0,v=p ; a=i,d=m
<ሽ ፍ ድ>	c=C
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ቁ ል ም ም>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቁ ል ጭ ል ጭ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ቁ ም ጥ>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ቁ ር ቁ ር>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቁ ር ብ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ቁ ስ ቁ ስ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቁ ን ን>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,v=0
<ቁ ን ድ ድ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቁ ን ጉ ል>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ቁ ን ጥ ር>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,v=0
<ቁ ን ጥ ን ጥ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ቁ ን ጽ ል>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቁ ጥ ብ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቁ ጥ እ>	c=A
  a=0,v=as ; a=0,v=p ; a=i,d=m
<ቁ ፍ ን ን>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ቅ ል ስ ል ስ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ቅ ል ብ ል ብ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ቅ ል ብ ስ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቅ ል ብ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቅ ል ጥ ል ጥ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ቅ ም ል>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቅ ም ጥ ል>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ቅ ም ጥ>	c=B
  a=0,v=as ; a=0,v=p ; a=i,d=m
<ቅ ር ም>	c=C
  a=0,v=0 ; a=0,v=p ; a=i,v=0
<ቅ ር ቅ ብ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,v=0
<ቅ ር ን እ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ቅ ር ድ ድ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቅ ስ ም>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,v=0
<ቅ ስ ር>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቅ ስ ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ቅ ስ ፍ ት>	c=F
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ቅ ስ ፍ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቅ ቅ ል>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቅ ብ ቅ ብ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቅ ብ ት ት>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቅ ብ ዝ ብ ዝ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ቅ ብ ጥ ር>	c=F
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ቅ ብ ጥ ብ ጥ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ቅ ብ ጥ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ቅ ት ር>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቅ ት ት>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ቅ ን ዝ ን ዝ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ቅ ን ጅ ይ>	c=E
  a=a,v=a ; a=a,v=p ; a=i,d=m
<ቅ ን ጥ ስ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቅ ን ጥ ብ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,v=0
<ቅ ን ጭ ር>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ቅ ን ፍ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቅ ዝ ን>	c=A
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ቅ ዝ ዝ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ቅ ዝ ፍ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቅ ዥ ይ>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ቅ ይ ል>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ቅ ጥ ን>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,v=0
<ቅ ጥ ፍ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቅ ጭ ል ጭ ል>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ቅ ጭ ል>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ቅ ጭ ጭ>	c=B
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ቅ ፍ ር ር>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቅ ፍ ቅ ፍ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቅ ፍ ድ ድ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቡ ል ት>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ቡ ት ር ፍ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቡ ን ን>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,v=0
<ቡ ዝ ን>	c=B
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ቡ ድ ስ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ቡ ድ ን>	c=C
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ቡ ጥ ጥ>	c=C
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ብ ል ዝ>	c=B
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ብ ል ግ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ብ ል ግ>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ብ ል ጥ ል ጥ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ብ ል ጥ ግ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ብ ል ጥ ጥ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ብ ል ጭ ል ጭ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ብ ል ጽ ግ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ብ ር ቅ ር ቅ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ብ ር ብ ር>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ብ ር ክ ር ክ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ብ ር ክ>	c=C
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ብ ር ዝ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,v=0
<ብ ር ግ ግ>	c=E
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ብ ስ ል ስ ል>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ብ ን ን>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ብ ን ን>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ብ እ ር እ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ብ ክ ት>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ብ ክ ን ክ ን>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ብ ው ዝ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ብ ው ዝ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ብ ይ ድ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ብ ግ ር>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,v=0
<ብ ግ ን>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ት ል ቅ>	c=B
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ት ል ት ል>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ት ል እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ት ር ኩ ስ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ት ር ክ ክ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ት ር ፍ ር ፍ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ት ብ ት ብ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ት ን ብ ይ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ት ኝ እ>	c=B
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ት እ ት እ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ት ኩ ር>	c=A
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ት ክ ት>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ት ክ ን>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ት ክ ዝ>	c=B
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ች ል ስ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ች ስ ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ች ብ ች ብ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ች ን ክ ር>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ች ክ ል>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ች ይ ክ>	c=A
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ች ፍ ች ፍ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ች ፍ ግ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ን ሁ ል ል>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ን ሱ ል ሱ ል>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ስ ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ን ስ ቅ ስ ቅ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ስ ን ስ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ን ስ ፍ ስ ፍ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ስ ፍ ፍ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ሹ ክ ክ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ሽ ር ት ት>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ሽ ት ት>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ሽ ው ር ር>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ሽ ፍ ፍ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ቁ ር ጥ ጥ>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ቁ ሽ ሽ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ቁ ጥ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ን ቅ ል ው ጥ>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ቅ ል ፍ እ>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ቅ ር ብ ብ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ቅ ስ ቅ ስ>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ቅ ስ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ን ቅ ብ ር ር>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ቅ ብ ቅ ብ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ቅ ው ል ል>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ቅ ዝ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,v=0
<ን ቅ ዥ ቅ ዥ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ቅ ጥ ቅ ጥ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ቅ ፍ ድ ድ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ቡ ል ቡ ል>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ቡ ግ ቡ ግ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ቡ ጭ ቡ ጭ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ብ ል ብ ል>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ብ ር ክ ክ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ብ ሽ ብ ሽ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ብ ን ብ>	c=E
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ብ ዝ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ን ቱ ስ ቱ ስ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ት ር ስ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ት ር ክ ክ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ት ብ ት ብ>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ት ክ ት ክ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ት ግ ት ግ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ች እ ች እ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ኝ ይ>	c=C
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ን እ ጥ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ን ኩ እ ኩ እ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ክ ል ው ስ>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ክ ር ት ት>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ክ ር ፍ ፍ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ክ ብ ል ል>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ክ ት>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,v=0
<ን ክ ው ት ት>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ክ ፍ ር ር>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ዝ ል ዝ ል>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ዝ ር ፍ ፍ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ዝ ር>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ን ዝ እ ዝ እ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ዝ ፍ ዝ ፍ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ዝ ፍ ጥ ጥ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ዥ ር ግ ግ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ዥ ቅ ዥ ቅ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ዥ ብ ር ር>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ዥ ብ ብ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ዱ ል ዱ ል>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ድ ል ቅ ቅ>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ድ ር ብ ብ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ድ ር ክ ክ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ድ ቅ ድ ቅ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ድ ብ ል ል>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ድ ብ ድ ብ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ድ ፍ ድ ፍ>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ጅ ል ጅ ል>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ጅ ር ግ ግ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ጉ ል ል>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ጉ ር ድ ድ>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ግ ል ት እ>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ግ ል ው ድ>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ግ ል ጅ ጅ>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ግ ር ብ ብ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ግ ር ግ ብ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ግ ሽ ግ ሽ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ግ ብ ግ ብ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ግ ብ>	c=A
  a=0,v=a ; a=0,v=as ; a=i,d=m
<ን ግ እ ግ እ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ግ ው ል ል>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ግ ድ ድ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ግ ጥ ጥ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ግ ጭ ግ ጭ>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ግ ፍ ግ ፍ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ግ ፍ ጥ ጥ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ጡ ል ጡ ል>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ጥ ር ር እ>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ጥ ር ብ ብ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ጥ ር ው ዝ>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ጥ ር ዝ ዝ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ጥ ር ጥ ስ>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ጥ እ ጥ እ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ጥ ፍ ጥ ፍ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ጭ ን ጭ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ጭ እ ጭ እ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ጽ ር>	c=A
  a=i,d=m ; a=i,v=a ; a=i,v=p
<ን ጽ ብ ር ቅ>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ፉ ቅ ቅ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ፉ እ ፉ እ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ፍ ል ስ ስ>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ፍ ር ግ ጥ>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ፍ ር ፍ ር>	c=H
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ፍ ቅ ፍ ቅ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ን ፍ ጥ>	c=A
  a=a,v=a ; a=a,v=p ; a=i,d=m
<እ ል ል>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<እ ል ም>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<እ ል ብ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<እ ም ስ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<እ ም ቅ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<እ ር ፍ>	c=A
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<እ ሽ ም>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<እ ቅ ድ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<እ ብ ብ>	c=B
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<እ ብ ድ>	c=A
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<እ ት ት>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<እ ን ቅ ፍ>	c=E
  a=0,v=as ; a=0,v=p ; a=i,d=m
<እ ን ግ ት>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<እ ን ጥ ስ>	c=E
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<እ ን ጥ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<እ ኝ ክ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<እ ው ስ>	c=A
  a=0,v=ast ; a=0,v=p ; a=i,d=m
<እ ው ድ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<እ ዝ ል>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<እ ይ ል>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<እ ድ ብ>	c=A
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<እ ድ ፍ>	c=A
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<እ ጅ ል>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<እ ጉ ር>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<እ ግ ስ>	c=B
  a=0,v=a ; a=0,v=p ; a=i,d=m
<እ ግ ት>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<እ ግ ድ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<እ ግ ግ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<እ ጥ ን>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<እ ጥ ፍ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,v=0
<እ ጭ ቅ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<እ ጭ ድ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,v=0
<ኩ ል ል>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ኩ ል ት ፍ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ኩ ል እ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ኩ ል ኩ ል>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ኩ ር ም ት>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ኩ ር ት>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ኩ ር ኩ ር>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ኩ ር ፍ ር ፍ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ኩ ስ ም ን>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ኩ ን ስ ን ስ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ክ ል ብ ስ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ክ ል ፍ ል ፍ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ክ ም ክ ም>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ክ ር ብ ት>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ክ ር ት ፍ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ክ ር ክ ም>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ክ ስ ም>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ክ ስ ብ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ክ ሽ ን>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ክ ብ ስ ብ ስ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ክ ት ም>	c=B
  a=0,v=0 ; a=0,v=a ; a=i,v=0
<ክ ት ር>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ክ ት ፍ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ክ ን ብ ል>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ክ ን ው ን>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ክ ን ድ እ>	c=E
  a=0,v=0 ; a=0,v=as ; a=i,v=0
<ክ እ ፍ እ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ክ ድ ም>	c=C
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ክ ድ ን>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ክ ፍ ን>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ክ ፍ ክ ፍ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ው ህ ድ>	c=A
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ው ል ል>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,v=0
<ው ል ብ ል ብ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ው ል ክ ፍ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ው ል ው ል>	c=F
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ው ር ዝ እ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ው ር ግ ር ግ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ው ስ ል ት>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ው ስ ብ>	c=A
  a=i,d=m ; a=i,v=a ; a=i,v=p
<ው ስ ድ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ው ሽ ቅ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ው ብ ቅ>	c=B
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ው ት ር ት ር>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ው ት ብ ት ብ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ው ት ው ት>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ው ት ፍ ት ፍ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ው ት ፍ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ው ኝ ይ>	c=C
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ው ዝ ግ ዝ ግ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ው ዝ ፍ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ው ይ ብ>	c=B
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ው ድ ል>	c=B
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ው ድ ም>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ው ግ ር>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,v=0
<ው ጥ ቅ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ው ፍ ር>	c=B
  a=0,v=0 ; a=0,v=a ; a=i,v=0
<ዝ ል ዝ ል>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ዝ ል ፍ ል ፍ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ዝ ም ም>	c=A
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ዝ ም ዝ ም>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ዝ ም ድ>	c=C
  a=0,v=as ; a=0,v=p ; a=i,d=m
<ዝ ር ብ ር ብ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ዝ ር ን ቅ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ዝ ር ክ ር ክ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ዝ ር ዝ ር>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ዝ ር ግ ፍ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ዝ ር ጥ ር ጥ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ዝ ር ፍ ር ፍ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ዝ ቅ ጥ>	c=B
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ዝ ብ ን ን>	c=F
  a=0,v=as ; a=0,v=p ; a=i,d=m
<ዝ ን ብ ል>	c=E
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ዝ ን ት ር>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ዝ ን ጥ ፍ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ዝ እ ል>	c=A
  a=0,v=0 ; a=0,v=as ; a=i,v=0
<ዝ እ ቅ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ዝ እ ግ>	c=A
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ዝ ክ ዝ ክ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ዝ ዝ ን>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ዝ ይ ን>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ዝ ይ ድ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ዝ ጉ ር ጉ ር>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ዝ ጉ ን>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ዝ ግ ር ር>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ዝ ግ ን>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ዝ ግ ይ ይ>	c=E
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ዝ ፍ ዝ ፍ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ዥ ል ጥ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ዥ እ ዥ እ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ዥ ጉ ር ጉ ር>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ዥ ጉ ድ ጉ ድ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ዱ ል ት>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ዱ ል ዱ ም>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ድ ህ ይ ይ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ድ ል ዝ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ድ ል ጥ>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ድ ም ስ ስ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ድ ም ን>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ድ ም ድ ም>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ድ ር ስ ም>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ድ ር ቅ ር ቅ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ድ ር ግ ም>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ድ ስ ስ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ድ ስ ት>	c=B
  a=0,v=as ; a=0,v=p ; a=i,d=m
<ድ ሽ ቅ>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ድ ሽ ይ ይ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ድ ቅ ን>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ድ ቅ ድ ቅ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ድ ቡ ል ቡ ል>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ድ ብ ል ል>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ድ ብ ል ብ ል>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ድ ብ ስ ብ ስ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ድ ብ ት>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ድ ብ ን>	c=B
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ድ ብ ዝ ዝ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ድ ብ ይ ይ>	c=F
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ድ ን ቅ ር>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ድ ን ዝ ዝ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ድ ን ዝ>	c=B
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ድ ን ድ ን>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ድ ን ግ ዝ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ድ ን ግ ግ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ድ ን ፍ እ>	c=E
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ድ እ ህ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ድ እ ስ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ድ ው ር>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ድ ድ ር>	c=B
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ድ ድ ቅ>	c=B
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ድ ድ ብ>	c=B
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ድ ግ ት>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ድ ፍ ን ፍ ን>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ድ ፍ ጥ ጥ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ድ ፍ ጥ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጅ ን ን>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,v=0
<ጉ ል ጉ ል>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጉ ም ር እ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጉ ም ጅ ይ>	c=E
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ጉ ም ጥ ም ጥ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ጉ ር ብ ር ብ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ጉ ር ብ ት>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ጉ ር ብ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጉ ር ን እ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጉ ር ፍ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጉ ስ ም>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጉ ብ ጉ ብ>	c=E
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ጉ ብ ጥ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጉ ት ን>	c=B
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጉ ት ጉ ት>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጉ ን ቁ ል>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጉ ን ብ ስ>	c=E
  a=0,v=a ; a=0,v=as ; a=i,d=m
<ጉ ን ጥ ፍ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ጉ እ ን>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጉ እ ጉ እ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጉ ዝ ጉ ዝ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጉ ድ ድ>	c=C
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጉ ድ ጉ ድ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጉ ጉ ል>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጉ ፍ ር>	c=B
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ግ ል ሙ ት>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ግ ል ም እ>	c=E
  a=0,v=0 ; a=a,v=a ; a=i,d=m
<ግ ል ብ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ግ ል ፍ ፍ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ግ ም ድ ል>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ግ ር ም ም>	c=E
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ግ ር ድ>	c=C
  a=0,v=0 ; a=0,v=p ; a=i,v=0
<ግ ር ጅ ፍ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ግ ር ግ ድ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ግ ር ጥ>	c=C
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ግ ስ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ግ ሽ ል ጥ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ግ ሽ ር>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ግ ሽ ሽ>	c=B
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ግ ሽ ብ>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ግ ብ ስ ብ ስ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ግ ብ ድ ድ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ግ ት ል ት ል>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ግ ት ር ት ር>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ግ ን ዝ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ግ ን ግ ን>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ግ እ ግ እ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ግ ዝ ግ ዝ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ግ ዝ ፍ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ግ ድ ር ድ ር>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ግ ድ ብ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ግ ድ ፍ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ግ ግ ር>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ግ ግ ር>	c=C
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ግ ጥ ግ ጥ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ግ ፍ ል ፍ ል>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ግ ፍ ግ ፍ>	c=E
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ግ ፍ ጥ>	c=C
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ጥ ል ቅ ል ቅ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ጥ ም ል ም ል>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ጥ ም ስ ም ስ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ጥ ም ዝ ም ዝ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ጥ ም ጥ ም>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጥ ር ም ስ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጥ ር ብ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጥ ር ዝ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጥ ቅ ጥ ቅ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጥ ብ ስ ቅ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጥ ን ስ ስ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጥ ን ቅ ር>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ጥ ን ብ እ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጥ ን ን>	c=B
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጥ ን ዝ እ>	c=E
  a=0,v=0 ; a=a,v=a ; a=i,d=m
<ጥ ን ፍ ፍ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጥ እ ድ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጥ ው ል ግ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጥ ው ም>	c=A
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ጥ ው ር>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጥ ው ዝ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጥ ይ ም>	c=B
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጥ ይ ቅ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጥ ይ ን>	c=A
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ጥ ድ ፍ>	c=A
  a=a,v=a ; a=a,v=p ; a=i,d=m
<ጥ ፍ ር>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጭ ል ም>	c=B
  a=0,v=0 ; a=0,v=a ; a=i,v=0
<ጭ ል ጥ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጭ ል ፍ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጭ ም ቅ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጭ ም እ>	c=C
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጭ ር ም ም>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ጭ ር ም ድ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ጭ ር ት>	c=C
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ጭ ቅ ይ ይ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጭ ብ ር ብ ር>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ጭ እ ጭ እ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጭ ው ል>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጭ ፍ ን>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጭ ፍ ግ ግ>	c=E
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ጵ ጵ ስ>	c=B
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ጽ ን ስ>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጽ ን ን>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጽ ው ም>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ጽ ይ ፍ>	c=B
  a=0,v=as ; a=0,v=p ; a=i,d=m
<ጽ ጽ ት>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ፉ ክ ት>	c=B
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ፍ ል ስ ፍ>	c=E
  a=a,v=a ; a=a,v=p ; a=i,d=m
<ፍ ል ቅ ል ቅ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ፍ ል ቅ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ፍ ል ክ ል ክ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ፍ ር ቅ ር ቅ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ፍ ር ክ ር ክ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ፍ ር ጥ ም>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ፍ ር ጥ ር ጥ>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ፍ ር ጥ ጥ>	c=E
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ፍ ር ጥ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ፍ ስ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ፍ ስ ክ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ፍ ት ል ክ>	c=E
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ፍ ት ል>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ፍ ት ፍ ት>	c=E
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ፍ ን ድ ቅ>	c=E
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ፍ ን ድ እ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ፍ ን ግ ል>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ፍ ን ግ ጥ>	c=E
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ፍ ን ጥ ዝ>	c=E
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ፍ ን ጥ ጥ>	c=F
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ፍ ን ፍ ን>	c=E
  a=a,v=a ; a=a,v=p ; a=i,d=m
<ፍ ክ እ>	c=A
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ፍ ው ስ>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ፍ ድ ስ>	c=C
  a=0,v=0 ; a=0,v=a ; a=i,d=m
<ፍ ግ ም>	c=B
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ፍ ግ ግ>	c=A
  a=0,v=0 ; a=0,v=as ; a=i,d=m
<ፍ ጥ ር>	c=A
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ፍ ጥ ፍ ጥ>	c=E
  a=0,v=0 ; a=0,v=p ; a=i,d=m
<ፍ ጭ ር ጭ ር>	c=G
  a=0,v=a ; a=0,v=p ; a=i,d=m
<ል ሽ ል ሽ>	c=E
  a=0,v=0 ; a=i,d=m
<ል ኩ ስ ኩ ስ>	c=G
  a=0,v=a ; a=i,d=m
<ል ኩ ፍ>	c=B
  a=0,v=0 ; a=i,d=m
<ል ክ ል ክ>	c=E
  a=0,v=a ; a=i,d=m
<ል ጉ ም ጉ ም>	c=G
  a=0,v=a ; a=i,d=m
<ል ፍ ጭ ቅ>	c=F
  a=0,v=a ; a=i,d=m
<ሙ ል ሙ ል>	c=E
  a=0,v=0 ; a=i,d=m
<ሙ ር ሙ ር>	c=E
  a=0,v=0 ; a=i,d=m
<ሙ ሽ ሽ>	c=C
  a=0,v=0 ; a=i,d=m
<ሙ ክ ክ>	c=B
  a=0,v=0 ; a=i,d=m
<ሙ ዝ ዝ>	c=B
  a=0,v=0 ; a=i,d=m
<ሙ ግ ግ>	c=B
  a=0,v=0 ; a=i,d=m
<ሙ ጥ ሙ ጥ>	c=E
  a=0,v=a ; a=i,d=m
<ሙ ጭ ሙ ጭ>	c=E
  a=0,v=0 ; a=i,d=m
<ም ል ግ>	c=C
  a=0,v=0 ; a=i,d=m
<ም ር ኩ ዝ>	c=E
  a=0,v=p ; a=i,d=m
<ም ስ ኩ እ>	c=E
  a=0,v=a ; a=i,d=m
<ም ስ ክ ን>	c=E
  a=0,v=0 ; a=i,d=m
<ም ን ግ ግ>	c=E
  a=0,v=0 ; a=i,d=m
<ም ን ጭ ር>	c=E
  a=0,v=0 ; a=i,d=m
<ም ክ ኝ ይ>	c=F
  a=0,v=a ; a=i,d=m
<ም ው ጭ>	c=A
  a=0,v=0 ; a=i,d=m
<ም ድ ም ድ>	c=E
  a=0,v=0 ; a=i,d=m
<ም ጥ ም ጥ>	c=E
  a=0,v=0 ; a=i,d=m
<ም ጽ ድ ቅ>	c=F
  a=0,v=p ; a=i,d=m
<ር ም ጥ>	c=B
  a=0,v=0 ; a=i,d=m
<ር ዝ ር ዝ>	c=E
  a=0,v=0 ; a=i,d=m
<ር ዝ ቅ>	c=B
  a=0,v=0 ; a=i,d=m
<ር ዥ ይ>	c=C
  a=0,v=a ; a=i,d=m
<ር ጥ ር ጥ>	c=E
  a=0,v=a ; a=i,d=m
<ስ ር ን ቅ>	c=E
  a=0,v=p ; a=i,d=m
<ስ ስ ን>	c=B
  a=0,v=0 ; a=i,d=m
<ስ ቅ ዝ>	c=B
  a=0,v=0 ; a=i,d=m
<ስ ቅ ጥ ጥ>	c=E
  a=0,v=0 ; a=i,d=m
<ስ ብ ስ ብ>	c=F
  a=0,v=0 ; a=i,d=m
<ስ ን ብ ጥ>	c=E
  a=0,v=0 ; a=i,d=m
<ስ ን ኝ>	c=B
  a=0,v=0 ; a=i,d=m
<ስ ን ፍ ጥ>	c=E
  a=0,v=0 ; a=i,d=m
<ስ እ ን>	c=A
  a=0,v=p ; a=i,d=m
<ስ ክ ስ ክ>	c=E
  a=0,v=0 ; a=i,d=m
<ስ ው ጥ>	c=A
  a=0,v=as ; a=i,d=m
<ስ ጉ ድ>	c=B
  a=0,v=0 ; a=i,d=m
<ስ ፍ ስ ፍ>	c=E
  a=0,v=as ; a=i,d=m
<ሹ ክ ክ>	c=B
  a=0,v=0 ; a=i,d=m
<ሹ ጥ ጥ>	c=A
  a=0,v=0 ; a=i,v=0
<ሽ ል ሽ ል>	c=E
  a=0,v=0 ; a=i,d=m
<ሽ ል ብ>	c=B
  a=0,v=as ; a=i,d=m
<ሽ ል ግ>	c=B
  a=0,v=0 ; a=i,d=m
<ሽ ሙ ጥ ጥ>	c=F
  a=0,v=a ; a=i,d=m
<ሽ ም ድ ድ>	c=E
  a=0,v=0 ; a=i,d=m
<ሽ ም ጥ ጥ>	c=E
  a=0,v=0 ; a=i,d=m
<ሽ ር ድ ድ>	c=E
  a=0,v=0 ; a=i,d=m
<ሽ ቅ ሽ ቅ>	c=E
  a=0,v=0 ; a=i,d=m
<ሽ ብ ር ቅ>	c=E
  a=0,v=as ; a=i,d=m
<ሽ ብ ት>	c=B
  a=0,v=0 ; a=i,d=m
<ሽ ን ቅ ር>	c=E
  a=0,v=0 ; a=i,d=m
<ሽ ን ቅ ጥ>	c=E
  a=0,v=0 ; a=i,d=m
<ሽ ን ክ ፍ>	c=E
  a=0,v=0 ; a=i,d=m
<ሽ ን ድ ር>	c=E
  a=0,v=0 ; a=i,d=m
<ሽ ን ጥ>	c=B
  a=0,v=0 ; a=i,d=m
<ሽ ክ ፍ>	c=B
  a=0,v=0 ; a=i,d=m
<ሽ ጉ ጥ ጥ>	c=F
  a=0,v=a ; a=i,d=m
<ሽ ግ ት>	c=C
  a=0,v=0 ; a=i,d=m
<ሽ ፍ ጥ>	c=B
  a=0,v=0 ; a=i,d=m
<ሽ ፍ ፍ>	c=B
  a=0,v=0 ; a=i,d=m
<ቁ ል ም ጥ>	c=F
  a=0,v=a ; a=i,d=m
<ቁ ም ጥ>	c=A
  a=0,v=0 ; a=i,d=m
<ቁ ር ፍ ድ>	c=E
  a=0,v=0 ; a=i,d=m
<ቁ ን ስ>	c=B
  a=0,v=0 ; a=i,d=m
<ቅ ል ም ድ>	c=F
  a=0,v=0 ; a=i,d=m
<ቅ ል ሽ ል ሽ>	c=G
  a=0,v=a ; a=i,d=m
<ቅ ር ሽ ይ>	c=E
  a=0,v=a ; a=i,d=m
<ቅ ር ን>	c=C
  a=0,v=p ; a=i,d=m
<ቅ ብ ዝ>	c=C
  a=0,v=0 ; a=i,d=m
<ቅ ብ ጅ ር>	c=F
  a=0,v=0 ; a=i,d=m
<ቅ ን ብ ጥ>	c=E
  a=0,v=a ; a=i,d=m
<ቅ ን ድ ብ>	c=E
  a=0,v=0 ; a=i,d=m
<ቅ እ ት>	c=A
  a=0,v=a ; a=i,d=m
<ቅ ይ ም>	c=A
  a=0,v=a ; a=i,d=m
<ቅ ጭ ም>	c=B
  a=0,v=0 ; a=i,d=m
<ቡ ር ቅ>	c=B
  a=0,v=0 ; a=i,d=m
<ቡ ክ ቡ ክ>	c=E
  a=0,v=0 ; a=i,d=m
<ቡ ግ ት>	c=C
  a=0,v=0 ; a=i,d=m
<ብ ር ቅ>	c=C
  a=0,v=0 ; a=i,d=m
<ብ ቅ ት>	c=B
  a=0,v=0 ; a=i,d=m
<ብ ዝ ቅ>	c=C
  a=0,v=0 ; a=i,d=m
<ቱ ስ ቱ ስ>	c=E
  a=0,v=a ; a=i,d=m
<ቱ ፍ ቱ ፍ>	c=E
  a=0,v=a ; a=i,d=m
<ት ር ብ>	c=B
  a=0,v=0 ; a=i,d=m
<ት ን ት ግ>	c=E
  a=0,v=0 ; a=i,d=m
<ት ን ኩ ል>	c=F
  a=0,v=p ; a=i,d=m
<ት ን ፍ ግ>	c=E
  a=0,v=0 ; a=i,d=m
<ት ክ ት ክ>	c=E
  a=0,v=0 ; a=i,d=m
<ች ር ች ም>	c=E
  a=0,v=0 ; a=i,d=m
<ች ር ች ር>	c=E
  a=0,v=0 ; a=i,d=m
<ን ር ት>	c=B
  a=0,v=0 ; a=i,d=m
<ን ስ ን ስ>	c=F
  a=0,v=0 ; a=i,d=m
<ን ሽ ጥ>	c=B
  a=0,v=0 ; a=i,d=m
<ን ቅ ር ር>	c=F
  a=0,v=a ; a=i,d=m
<ን ቡ ት ር>	c=F
  a=0,v=a ; a=i,d=m
<ን ቡ ጭ>	c=B
  a=0,v=0 ; a=i,d=m
<ን ብ ር ቅ>	c=F
  a=0,v=a ; a=i,d=m
<ን ት ል ክ ስ>	c=H
  a=0,v=a ; a=i,d=m
<ን ት ብ>	c=A
  a=0,v=0 ; a=i,d=m
<ን ኩ ፍ ፍ>	c=F
  a=0,v=p ; a=i,d=m
<ን ዝ ር ጥ>	c=F
  a=0,v=a ; a=i,d=m
<ን ድ ክ ድ ክ>	c=G
  a=0,v=a ; a=i,d=m
<ን ጉ ር ጉ ር>	c=H
  a=0,v=a ; a=i,d=m
<ን ጉ ድ ድ>	c=F
  a=0,v=p ; a=i,d=m
<ን ግ ል ል>	c=F
  a=0,v=p ; a=i,d=m
<ን ግ ር ግ ር>	c=H
  a=0,v=a ; a=i,d=m
<ን ጥ ል ል>	c=F
  a=0,v=p ; a=i,d=m
<እ ል ጥ>	c=B
  a=0,v=0 ; a=i,d=m
<እ ም ግ>	c=B
  a=0,v=0 ; a=i,d=m
<እ ም ጥ>	c=A
  a=0,v=0 ; a=i,d=m
<እ ር ብ>	c=B
  a=0,v=0 ; a=i,d=m
<እ ር ዝ>	c=A
  a=0,v=p ; a=i,d=m
<እ ር ጥ>	c=B
  a=0,v=0 ; a=i,d=m
<እ ት ብ>	c=A
  a=0,v=0 ; a=i,d=m
<እ ዥ ይ>	c=A
  a=0,v=0 ; a=i,d=m
<እ ግ ም>	c=A
  a=0,v=0 ; a=i,d=m
<እ ፍ ፍ>	c=B
  a=0,v=0 ; a=i,d=m
<ኩ ም ኩ ም>	c=E
  a=0,v=0 ; a=i,d=m
<ኩ ር ሽ ም>	c=E
  a=0,v=0 ; a=i,d=m
<ኩ ር ጥ>	c=B
  a=0,v=0 ; a=i,d=m
<ኩ ብ ኩ ብ>	c=E
  a=0,v=a ; a=i,d=m
<ኩ ን ት ር>	c=F
  a=0,v=p ; a=i,d=m
<ኩ ፍ ስ>	c=B
  a=0,v=p ; a=i,d=m
<ኩ ፍ ኩ ፍ>	c=E
  a=0,v=0 ; a=i,d=m
<ክ ል ፍ>	c=B
  a=0,v=0 ; a=i,d=m
<ክ ር ድ ድ>	c=E
  a=0,v=0 ; a=i,d=m
<ክ ር ፍ እ>	c=E
  a=0,v=0 ; a=i,d=m
<ክ ብ ስ>	c=A
  a=0,v=0 ; a=i,d=m
<ክ ች ር>	c=B
  a=0,v=0 ; a=i,d=m
<ክ ን ት ር>	c=E
  a=0,v=0 ; a=i,d=m
<ክ ን ክ ን>	c=E
  a=0,v=0 ; a=i,d=m
<ክ ን ፍ>	c=A
  a=0,v=0 ; a=i,d=m
<ው ስ ው ስ>	c=E
  a=0,v=p ; a=i,d=m
<ው ሽ ል>	c=B
  a=0,v=0 ; a=i,d=m
<ው ሽ ክ ት>	c=E
  a=0,v=0 ; a=i,d=m
<ው ሽ ክ>	c=C
  a=0,v=a ; a=i,d=m
<ው ት ት>	c=C
  a=0,v=0 ; a=i,v=0
<ው ን ው ን>	c=E
  a=0,v=0 ; a=i,d=m
<ው ን ፍ ል>	c=F
  a=0,v=p ; a=i,d=m
<ው ድ ል ድ ል>	c=G
  a=0,v=a ; a=i,d=m
<ው ጭ ም ድ>	c=F
  a=0,v=p ; a=i,d=m
<ው ፍ ፍ>	c=B
  a=0,v=0 ; a=i,d=m
<ዝ ል ስ>	c=B
  a=0,v=0 ; a=i,d=m
<ዝ ል ብ ድ>	c=F
  a=0,v=0 ; a=i,d=m
<ዝ ር ጥ ጥ>	c=E
  a=0,v=0 ; a=i,d=m
<ዝ ር ጥ>	c=A
  a=0,v=as ; a=i,d=m
<ዝ ር ፍ ጥ>	c=E
  a=0,v=p ; a=i,d=m
<ዝ ብ ል ል>	c=E
  a=0,v=0 ; a=i,d=m
<ዝ ብ ን>	c=B
  a=0,v=0 ; a=i,d=m
<ዝ ብ ዝ ብ>	c=E
  a=0,v=0 ; a=i,d=m
<ዝ ት ል>	c=B
  a=0,v=0 ; a=i,d=m
<ዝ ት ል>	c=C
  a=0,v=0 ; a=i,d=m
<ዝ ን ቁ ል>	c=E
  a=0,v=0 ; a=i,d=m
<ዝ ን ክ ት>	c=F
  a=0,v=p ; a=i,d=m
<ዝ ን ጥ>	c=B
  a=0,v=0 ; a=i,d=m
<ዝ ን ፍ ል>	c=F
  a=0,v=p ; a=i,d=m
<ዝ ግ ን ን>	c=E
  a=0,v=0 ; a=i,d=m
<ዝ ጥ ዝ ጥ>	c=E
  a=0,v=as ; a=i,d=m
<ዥ ር ግ ግ>	c=E
  a=0,v=0 ; a=i,d=m
<ዥ ዥ ይ>	c=C
  a=0,v=0 ; a=i,d=m
<ዱ ፍ ዱ ፍ>	c=E
  a=0,v=0 ; a=i,d=m
<ድ ል ፍ ስ>	c=E
  a=0,v=0 ; a=i,d=m
<ድ ስ ም>	c=B
  a=0,v=0 ; a=i,d=m
<ድ ሽ ድ ሽ>	c=E
  a=0,v=a ; a=i,d=m
<ድ ቁ ን>	c=C
  a=0,v=a ; a=i,d=m
<ድ ብ ስ ስ>	c=E
  a=0,v=0 ; a=i,d=m
<ድ ን ቁ ል>	c=E
  a=0,v=p ; a=i,d=m
<ድ ን ብ እ>	c=E
  a=0,v=0 ; a=i,d=m
<ድ ን ጉ ር>	c=E
  a=0,v=0 ; a=i,d=m
<ድ እ ጭ>	c=A
  a=0,v=0 ; a=i,d=m
<ድ ክ ር>	c=C
  a=0,v=0 ; a=i,d=m
<ድ ዝ ድ ዝ>	c=E
  a=0,v=a ; a=i,d=m
<ድ ጉ ስ>	c=B
  a=0,v=0 ; a=i,d=m
<ጅ ር ግ ግ>	c=E
  a=0,v=0 ; a=i,d=m
<ጅ ብ ድ>	c=B
  a=0,v=0 ; a=i,d=m
<ጅ ጅ ይ>	c=C
  a=0,v=0 ; a=i,d=m
<ጉ ል ም ም>	c=F
  a=0,v=p ; a=i,d=m
<ጉ ል ድ ፍ>	c=F
  a=0,v=p ; a=i,d=m
<ጉ ም ል ል>	c=F
  a=0,v=p ; a=i,d=m
<ጉ ም ጥ>	c=C
  a=0,v=a ; a=i,d=m
<ጉ ር ም ር ም>	c=G
  a=0,v=a ; a=i,d=m
<ጉ ር ም ስ>	c=E
  a=0,v=0 ; a=i,d=m
<ጉ ር ብ ጥ>	c=E
  a=0,v=0 ; a=i,d=m
<ጉ ር ድ ም>	c=E
  a=0,v=0 ; a=i,d=m
<ጉ ር ድ>	c=A
  a=0,v=0 ; a=i,v=0
<ጉ ር ጉ ር>	c=E
  a=0,v=0 ; a=i,d=m
<ጉ ር ጥ ር ጥ>	c=G
  a=0,v=a ; a=i,d=m
<ጉ ስ ር>	c=B
  a=0,v=0 ; a=i,d=m
<ጉ ብ ብ>	c=A
  a=0,v=0 ; a=i,d=m
<ጉ ብ ዝ>	c=B
  a=0,v=0 ; a=i,d=m
<ጉ ብ ድ ድ>	c=E
  a=0,v=a ; a=i,d=m
<ጉ ት ም ት ም>	c=G
  a=0,v=a ; a=i,d=m
<ጉ ን ዝ ል>	c=F
  a=0,v=p ; a=i,d=m
<ጉ ን ጥ>	c=B
  a=0,v=0 ; a=i,d=m
<ጉ ን ፍ>	c=B
  a=0,v=0 ; a=i,d=m
<ጉ ድ ኝ ይ>	c=F
  a=0,v=p ; a=i,d=m
<ጉ ጉ ር>	c=C
  a=0,v=0 ; a=i,d=m
<ጉ ጉ ጥ>	c=C
  a=0,v=0 ; a=i,d=m
<ጉ ፍ ን ን>	c=E
  a=0,v=0 ; a=i,d=m
<ጉ ፍ ይ ይ>	c=E
  a=0,v=0 ; a=i,d=m
<ግ ል ድ ም>	c=E
  a=0,v=a ; a=i,d=m
<ግ ል ጅ ጅ>	c=E
  a=0,v=0 ; a=i,d=m
<ግ ል ፍ ጥ>	c=E
  a=0,v=0 ; a=i,d=m
<ግ ም ል>	c=B
  a=0,v=0 ; a=i,d=m
<ግ ር ሽ ይ>	c=E
  a=0,v=a ; a=i,d=m
<ግ ር ድ ፍ>	c=E
  a=0,v=0 ; a=i,d=m
<ግ ስ ር>	c=A
  a=0,v=0 ; a=i,d=m
<ግ ስ ግ ስ>	c=E
  a=0,v=0 ; a=i,d=m
<ግ ብ ስ>	c=C
  a=0,v=a ; a=i,d=m
<ግ ን ት ር>	c=E
  a=0,v=0 ; a=i,d=m
<ግ ን ድ ስ>	c=E
  a=0,v=0 ; a=i,d=m
<ግ ን ፍ እ>	c=E
  a=0,v=a ; a=i,d=m
<ግ ድ ግ ድ>	c=E
  a=0,v=0 ; a=i,d=m
<ግ ጥ ጥ>	c=C
  a=0,v=0 ; a=i,d=m
<ግ ፍ ር>	c=C
  a=0,v=a ; a=i,d=m
<ጥ ል ዝ>	c=B
  a=0,v=0 ; a=i,d=m
<ጥ ም ር ር>	c=E
  a=0,v=0 ; a=i,d=m
<ጥ ም ስ ስ>	c=E
  a=0,v=0 ; a=i,d=m
<ጥ ር ን ቅ>	c=E
  a=0,v=0 ; a=i,d=m
<ጥ ር ጥ ስ>	c=E
  a=0,v=0 ; a=i,d=m
<ጥ ስ ስ>	c=C
  a=0,v=0 ; a=i,d=m
<ጥ ስ ቅ>	c=B
  a=0,v=0 ; a=i,d=m
<ጥ ብ ር ብ ር>	c=G
  a=0,v=a ; a=i,d=m
<ጥ ብ ድ ል>	c=E
  a=0,v=0 ; a=i,d=m
<ጥ ብ ጥ ብ>	c=F
  a=0,v=0 ; a=i,d=m
<ጥ ት ት>	c=B
  a=0,v=p ; a=i,d=m
<ጥ ን ብ ስ>	c=F
  a=0,v=p ; a=i,d=m
<ጥ ን ብ ዝ>	c=E
  a=0,v=0 ; a=i,d=m
<ጥ ን ው ት>	c=F
  a=0,v=p ; a=i,d=m
<ጥ ው ል ው ል>	c=G
  a=0,v=a ; a=i,d=m
<ጥ ው ል>	c=B
  a=0,v=0 ; a=i,d=m
<ጥ ድ ቅ>	c=A
  a=0,v=a ; a=i,d=m
<ጥ ግ ግ>	c=B
  a=0,v=0 ; a=i,d=m
<ጩ ር ር>	c=A
  a=0,v=0 ; a=i,d=m
<ጭ ል ግ>	c=A
  a=0,v=a ; a=i,d=m
<ጭ ል ጭ ል>	c=E
  a=0,v=a ; a=i,d=m
<ጭ ር ም ት>	c=F
  a=0,v=p ; a=i,d=m
<ጭ ር ግ ድ>	c=E
  a=0,v=0 ; a=i,d=m
<ጭ ር ጭ ስ>	c=E
  a=0,v=0 ; a=i,d=m
<ጭ ቡ ድ>	c=A
  a=0,v=0 ; a=i,d=m
<ጭ ብ ት>	c=B
  a=0,v=p ; a=i,d=m
<ጭ ን ቁ ር>	c=E
  a=0,v=a ; a=i,d=m
<ፉ ክ ት>	c=C
  a=0,v=0 ; a=i,d=m
<ፉ ጭ ይ>	c=C
  a=0,v=a ; a=i,d=m
<ፍ ል ም>	c=C
  a=0,v=p ; a=i,d=m
<ፍ ስ ፍ ስ>	c=E
  a=0,v=0 ; a=i,d=m
<ፍ ሽ ግ>	c=C
  a=0,v=a ; a=i,d=m
<ፍ ቅ ፍ ቅ>	c=E
  a=0,v=0 ; a=i,d=m
<ፍ ን ች ር>	c=E
  a=0,v=p ; a=i,d=m
<ፍ ን ድ ድ>	c=E
  a=0,v=a ; a=i,d=m
<ፍ ክ ፍ ክ>	c=E
  a=0,v=a ; a=i,d=m
<ፍ ይ ል>	c=B
  a=0,v=0 ; a=i,d=m
