# Rezolvare Tema 4

## 1. CRC HTTP service
URL catre API-ul nostru este:
```

http://ec2-35-173-126-158.compute-1.amazonaws.com:8001/crc
```

## 2. Protocoale de routare

- ### **`Forwarding vs. Routing`**


`Forwarding–ul` este procesul de a trimite un pachet pe calea lui, adică se cunoaște ruta pe unde să o ia pachetul (se cunoaște următorul nod din drum). Pentru implementarea forwarding-ului se foloseste algoritmul `longest matching prefix` care funcționează astfel: 
-	Pentru fiecare pachet găsește cel mai lung prefix care conține destinația adresă (cea mai specifică intrare)
-	Trimite pachetul către următorul router pentru acel prefix
Acest algoritm utilizează o tabelă de prefixe de ip - uri (un prefix de ip reprezintă ip uri dintr-un anume interval), iar când se primește un ip se va căuta intervalul din care face acesta parte și se va trimite pachetul către respectiva zonă. Acest proces se va relua și pe următorul router pâna ce pachetul va ajunge la destinație.

`Routing-ul` este procesul de a decide în ce direcție trebuie trimis traficul. În acest caz nu se cunoaște calea către destinație și este necesar să se găsească cea mai scurtă cale (mai rapidă sau mai sigură (depinde de metrica utilizată)) către respectiva destinație. Astfel trebuie utilizate toate legăturile rețelei.

Există mai multe moduri de rutare, precum: load-sensitive routing, routing, traffic engineering, provisioning.
De asemenea există mai multe modele de rutare: unicast, broadcast, multicast, anycast.

Câteva dintre `obiectivele algoritmilor de rutare` sunt: *`corectitudinea` (să se găseasca un drum care este corect), `drum eficient` (să se utilizeze lățimea de bandă eficient), `drum echitabil` (să nu fie nici un nod în așteptare), `convergența rapidă` (să-și revină rapid după schimbări), `scalabilitate` (să funcționeze bine și când rețeaua se mărește)*.

Câteva dintre `regulile algoritmilor de rutare` sunt: *`toate nodurile sunt la fel` (nu există nici un controler), `nodurile știu doar ceea ce învață schimbând mesaje cu vecinii, nodurile operează concomitent`.*

`În concluzie`, în opinia mea asemănarea dintre aceste două protocoale este că ambele trimit pachetele mai departe în timp ce deosebirea majoră este că forwarding-ul știe exact unde să trimită respectivul pachet în timp ce rutarea trebuie să găsească cea mai scurtă cale până la destinație. De aceea forwarding-ul trebuie să se realizeze rapid, având în vedere că un router poate procesa milioane de pachete pe secundă.

- ### **`Link State Routing`**

  - Este o tehnica de rutare prin care orice router aflat in reteaua de internet isi imparte informatiile cu celelalte routere vecine.

  - Nodurile/Routerele isi cunosc doar costurile drumurilor dintre ele si vecinii lor.

   - In comunicarea cu cu celelalte noduri, routerele pot oferi doar informatii despre costul pana la vecinii lor, folosindu-se de mesaje.

  - Este necesar ca fiecare nod sa ruleze acelasi algoritm pentru a putea comunica.

  - Este posibil ca informatiile sa fie pierdute in timpul comunicarii.

  - In momentul punerii in functiune a unui router, acesta isi calculeaza costurile pana la vecinii sai, urmand ca aceste informatii sa fie trimise catre toate routerele vecine.

  - In timpul functionarii unui router, daca se schimba costul pana la unul din vecini, acesta retrimite un nou set de informatii actualizate tuturor vecinilor.

  - In urma acestui schimb de informatii "din aproape in aproape", fiecare router va fi capabil sa-si construiasca propria topologie/"harta" care va contine toate nodurile disponibile in acel moment in reteaua de internet, precum si costurile dintre fiecare 2 routere.

  - Fiecare router va folosi algoritmul lui Dijkstra pentru a afla rutele optime catre orice nod.
  
  - Datorita caracterului iterativ al algoritmului lui Dijkstra, este de ajuns calcularea distantelor pana la atingerea sursei.

- ### **`Distance Vector Routing`**

Este un algoritm de rutare `dinamic`, adică topologia poate suferi modificări algoritmul aflând cea mai bună cale pe noua topologie a rețelei. Mai este denumit algoritmul `Bellman-Ford` distribuit. 

Fiecare router rulează o instanță a acestui algoritm astfel că fiecare va cunoaște cea mai bună cale pentru un anume pachet. Fiecare folosește pentru implementarea algoritmului un vector de distanțe de la el pana la celelalte routere astfel că orice router va ști cea mai bună legatură pentru fiecare destinație. Aceste distanțe sunt actualizate pe baza schimbului de informții între vecini adică între routerele conectate în mod direct. De asemenea `ajunge greu la convergență` deoarece sunt necesare multe schimburi de informații.

Un `avantaj` al acestui algoritm este consumul redus de resurse astfel că este util în situațiile  în care există constrângeri privind resursele.

Totuși are un `dezavantaj major` și anume `The Count-to-Infinity Problem`. Aceasta constă în faptul că se va crea un ciclu infinit datorită unui router care nu mai poate fi accesat. De exemplu daca avem un drum `A - B – C` și routerul `C` nu mai poate fi contactat, în momentul în care pachetul care ajunge de la `A` la `B` și apoi ar trebui sa ajungă la `C`, acesta se va duce din nou la `A` (deoarece în tabela de rutare a lui `B` apare că se poate ajunge la `C` și prin `A`). Astfel pachetul ajunge la `A` care il trimite din nou la `B` (deoarece în tabela lui de rutare apare că la `C` se ajunge prin `B`). În momentul acestor schimburi se actualizează și costurile transmisiei, adică fiecare router ÎȘi va actualiza vectorul său de distanțe. Dar fiind un circuit se va incrementa până la infinit, de aici și numele acestei probleme.
S-a încercat rezolvarea acesteia prin adoptarea unor euristici (de ex: split horizon, poison reverse) însă nici una nu a rezolvat problema. 

Astăzi în practică protocoalele care utilizează algoritmul `link-state` sunt utilizate în locul acestuia.



- ### **`Routing Information Protocol`**

  - Unul dintre cele mai vechi protocoale de rutare. Este de tip distance vector.

  - Foloseste ca metrica de rutare numarul de pasi (hops).

  - Previne buclele de rutare prin setarea unui numar maxim de pasi de la sursa la destinatie. In general limita este setata la 15 pasi. Un drum de 16 pasi este considerat de lungime infinita. 

  - In primii ani de functionare, fiecare router capabil RIP transmitea la fiecare 30 de secunde tabela de rutare, fiind mult mai mici decat in prezent.

  - Un timeout de 180 de secunde rezulta in eliminarea unui router din topologie (failures).

  - Foloseste UDP ca protocol de transport si ii este atribuit portul 520.

  - Foloseste mecanisme pentru prevenirea propagarii de informatii incorecte (Split horizon, Route poisoning, holddown)

- ### **`Open Shortest Path First`**

`Open Shortest Path First(OSPF)` este un protocol care utilizează algoritmul `link-state routing(LSR)` și este un protocol intradomain routing (`interior gateway protocol`), adică este creat să funcționeze într-un sistem autonom. Ceea ce face OSPF este să reprezinte rețeaua reală ca un graf și apoi să folosească algoritmul link-state pentru ca fiecare router să calculeze cea mai scurtă cale de la sine la toate celelalte noduri. Se pot găsi mai multe căi care sunt la fel de scurte. În acest caz, OSPF își amintește setul de trasee cele mai scurte și în timpul redirecționării pachetelor, traficul este împărțit între ele, ceea ce ajuta la echilibrarea sarcinii transmise (`Equal Cost MultiPath – ECMP`).
Acesta este un protocol open source fiind extrem de utilizat în acest moment, majoritatea routerelor suportând acest protocol.


- ### **`Border Gateway Protocol Routing`**

  - Este un protocol de rutare bazat pe path-vector si pe politicile de rutare ale sistemelui autonom (AS) din care face parte

  - AS-urile influenteaza in mod direct calea pachetelor catre destinatie deoarece routerele comunica intre ele prin announcements-uri. Acestea din urma contin informatii cu privire la destinatie(prefix), istoricul drumului (Path vector) si urmatorul hop(router) prin care pachetul ar trebui sa isi continuie drumul. Toate aceste informatii sunt folosite pentru a respecta politica AS-ului dar si pentru a evita o eventuala bucla prin verificarea path vectorului.

  - Se poate asigura astfel un drum optim catre destinatie, bazat pe informatiile detinute de fiecare router si gestionate de AS-uri.

  - In general utilizarea BGP implica increderea in informatiile oferite de fiecare router.

  - In general, sistemele autonome (AS) apartin ISP-urilor sau marilor organizatii high-tech. Pentru a nu exista exploit-uri, AS-urile care doresc sa foloseasca BGP in comunicarea cu alte AS-uri (in mod extern - eBGP) au nevoie de un ASN (Autonomous System Number) emis de catre autoritatea IANA. Exista totusi exceptii notabile care au dus la o rutare a traficului deficitara.
 [BGP can break the Internet](https://www.cloudflare.com/learning/security/glossary/what-is-bgp/).
 Acest lucru se poate intampla atunci cand un AS anunta rute gresite (nu neaparat accidental) pe care routerele le vor crede de incredere si vor ruta traficul in acea directie.

  - Spre deosebire de celelalte protocoale de rutare, stabilește și menține conexiuni între routerele vecine folosind protocolul TCP. În cazul routerelor aflate în AS-uri diferite, o conexiune BGP poate fi stabilită doar dacă routerele sunt direct conectate. Legătura se realizează pe portul TCP 179, fiind menținută prin mesaje periodice de 19 octeți (intervalul implicit este de 60 de secunde).
