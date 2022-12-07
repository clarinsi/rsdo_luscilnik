# Luščilnik terminoloških kandidatov

## Delovanje

Luščilnik je izdelan kot spletna storitev, ki omogoča luščenje terminoloških kandidatov iz zbirke besedil uporabnika v običajnih datotečnih formatih za zapis besedil, kot tudi luščenje terminoloških kandidatov iz korpusa oss.

Spletna storitev omogoča celotno luščenje v enem samem koraku, zagon posameznih segmentov obdelave ter omogoča tako sinhrono delovanje, kot tudi asinhrono delovanje, kadar uporabnik storitve pričakuje, da bo čas luščenja prevelik.

Luščenje je mogoče izvajati na dva načina, pri čemer je bolj zapleten način luščenja terminov iz uporabniških besedil. Postopek luščenja je sledeč:

1. Pretvorba vhodnih datotek v čisto besedilo
2. Segmentacija in označevanje besedil z POS označevalnikom classla
3. Luščenje terminologije
4. Iskanje kanoničnih oblik
5. Iskanje dobrih primerov uporabe

Kadar gre za luščenje terminov iz korpusa OSS, uporabnik poda obseg besedil preko filtra leta, vrste dokumentov, ključnih besed in udk vrstilca. Ker so dokumenti že predobdelani (pretvorjeni in označeni) se 1. in 2. korak lahko preskočita.

Natančen opis klicev in uporabe storitev je dostopen na http://rsdo.lhrs.feri.um.si:8080/ui/

## Komponente

### Programski vmesnik za luščenje 

Programski vmesnik za luščenje sestavlja python flask strežnik, v katerem tečejo orkestracijske storitve, ki omogočajo izvajanje luščenja na način REST. Zraven teče še swagger strežnik z opisom api-ja, ki uporabnikom omogoča lažjo integracijo v svoje storitve. Vmesnikovo delovanje je odvisno od ostalih kompoment sistema.


### SloBERT luščilnik 

Programski vmesnik do luščilnika, naučenega na RSDO5 učnem korpusu, ki omogoča luščenje iz besedil v conllu obiliki.
Natančen opis in izvorni repoitorij dela projekta se nahaja na https://github.com/honghanhh/ate-docker

### Kanonizator besednih zvez 

Programski vmesnik do kanonizatorja besednih zvez, ki se uporablja za pretvorbo najdenih terminoloških kandidatov iz lematizirane ali neosnovne oblike, v kanonično obliko.
Natančen opis in izvorni repozitorij dela projekta se nahaja na: https://github.com/honghanhh/ate-docker

### Podatkovna baza korpusa OSS 

Podatkovna baza korpusa OSS vsebuje obdelana besedila iz korpusa OSS ter hkrati tudi iskalne indekse, ki omogočajo hitrejše poizvedbe po podatkih. Prav tako so v podatkovni bazi predizračunani hevristični indeksi za iskanje terminoloških kandidatov ter procedure za obdelavo uporabniških besedil na enak način. Ker je sama vsebina podatkovne baze prevelika, so dodane samo skripte za kreiranje strukture tabele, sam korpus pa je v bazo potrebno po instalaciji uvoziti in zagnati njegovo obdelavo.

Uporabljena je odprtokodna podatkovna baza MariaDB z ColumnStore hrambo. 

## Zahteve
Za izvajanje priporočamo docker izvajalno okolje
Posamezni deli imajo ločene zahteve, ki se lahko razberejo v Dockerfile skriptah


## Uporaba
Za zagon storitve je potrebno najprej ustrezno konfigurirati izvajaln okolje docker. To je možno preko datoteke docker_compose.yml. Ta je prednastavljena tako, da pričakuje, da bo v nadmapi izvorne kode ustvarjena mapa, v katero se bodo naložili jezikovni modeli, saj se tako ne prenaša v izvajalno okolje docker. Uporabnik lahko to seveda spremeni po želji.

Za uporabo korpusa OSS je potrebno slednjega ustrezno uvoziti v podatkovno bazo. Objavljen je na clarin.si 

Izgradnja slike se zažene z 

```
docker-compose build
```

zagon pa z 

```
docker-compose up
```

## Avtorji

Pri ustvarjanju projekta so sodelovali:
Marko Ferme, Hanh Thi Hong Tran, Klemen Kac, Matej Martinc, Milan Ojsteršek, Vid Podpečan, Senja Pollak, Marko Pranjić, Andraž Repar, Kristjan Žagar
