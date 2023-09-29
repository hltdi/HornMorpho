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

<ም ው ት>		c=A

<ስ ብ ር>		c=A			{ሰበረ}

<ል ብ ስ>		c=A			{ሰበረ}

<ን ግ ር>		c=A			{ነገረ}

<ቅ ር ብ>		c=A			{ሮጠ}

<ዝ ን ብ>		c=A			{ዘነበ}

<ግ ድ ል>		c=A

<ቍ ር ጥ>		c=A			{ሰበረ}

<ቁ ጥ ር>		c=A			{ሰበረ}

<ብ ር ር>		c=A			{ሮጠ}

<ጥ ቁ ር>		c=A

<ሽ ይ ጥ>		c=A			{ሰበረ}

<ግ ይ ጥ>		c=A

<እ ድ ር>		c=A

<እ ል ፍ>		c=A

<እ ብ ብ>		c=A

<ስ ም እ>	 	c=A			{ሰበረ}

<ብ ል እ>		c=A			{በላ}

<ፍ ት እ>		c=A			{በላ}

<ቅ ር ይ>		c=A			{ሮጠ}

<ስ ጥ ይ>		c=A			{ሰበረ}

<ስ እ ም>	     c=A			{ሳመ}

<እ ጥ እ>	     c=A			{አመመ}

<ይ እ ዝ>	     c=A			{ሳመ}

<ፍ ል ግ>	      c=B			{ሰበረ}

<ጭ ር ስ>	      c=B			{ሰበረ}

<ጭ ቁ ን>	      c=B

<ጥ ጥ እ>	      c=B			{ሰበረ}

<ል ክ እ>	      c=B

<ል ይ ይ>	      c=B

<እ ስ ብ>	      c=B

<ቅ ም ጥ>	      c=B			{ተቀመጠ}

<ብ ር ክ>	      c=C

<ቁ ጥ ር>	      c=C

<ቅ ጥ እ>	      c=C

<ል ጭ ይ>	      c=C

<ፉ ጭ ይ>	      c=C

<ጭ ፍ ጭ ፍ>     c=E

<ም ስ ክ ር>     c=E

<እ ን ክ ስ>     c=E

<ግ ን ብ እ>     c=E

<ስ ል ች ይ>     c=E

<ብ እ ብ እ>     c=E

<ሙ እ ሙ እ>   c=E

<ቅ ብ ጥ ር>     c=F

<ዝ ግ ጅ ይ>     c=F

<ዱ ል ዱ ም>     c=E

<ሙ ል ፍ ፍ>     c=E

<ሽ ር ሙ ጥ>      c=E

<ጭ ብ ር ብ ር>   c=G

<ን ኵ እ ኵ እ>   c=G

<ን ጭ እ ጭ እ>   c=G

<ሽ ሙ ን ሙ ን>   c=G

<ን ጽ ብ ር ቅ>   c=H

<ን ስ ፍ ፍ>     c=J
