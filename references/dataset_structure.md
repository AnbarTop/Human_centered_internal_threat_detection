# Estructura de los Datasets (CERT r4.2)

Este documento muestra la estructura básica (columnas, tipos de datos y ejemplos) de los datasets crudos a tener en cuenta en la fase de ingesta.

## Logon
- **Archivo:** `logon.csv`
- **Tamaño aprox:** `55.80 MB`

### Esquema
| Columna | Tipo de Dato (Pandas) |
|---------|-----------------------|
| `id` | `str` |
| `date` | `str` |
| `user` | `str` |
| `pc` | `str` |
| `activity` | `str` |

### Muestra (primeras 5 filas)
| id | date | user | pc | activity |
| --- | --- | --- | --- | --- |
| {X1D9-S0ES98JV-5357PWMI} | 01/02/2010 06:49:00 | NGF0157 | PC-6056 | Logon |
| {G2B3-L6EJ61GT-2222RKSO} | 01/02/2010 06:50:00 | LRR0148 | PC-4275 | Logon |
| {U6Q3-U0WE70UA-3770UREL} | 01/02/2010 06:53:04 | LRR0148 | PC-4124 | Logon |
| {I0N5-R7NA26TG-6263KNGM} | 01/02/2010 07:00:00 | IRM0931 | PC-7188 | Logon |
| {D1S0-N6FH62BT-5398KANK} | 01/02/2010 07:00:00 | MOH0273 | PC-6699 | Logon |

## Device
- **Archivo:** `device.csv`
- **Tamaño aprox:** `27.64 MB`

### Esquema
| Columna | Tipo de Dato (Pandas) |
|---------|-----------------------|
| `id` | `str` |
| `date` | `str` |
| `user` | `str` |
| `pc` | `str` |
| `activity` | `str` |

### Muestra (primeras 5 filas)
| id | date | user | pc | activity |
| --- | --- | --- | --- | --- |
| {J1S3-L9UU75BQ-7790ATPL} | 01/02/2010 07:21:06 | MOH0273 | PC-6699 | Connect |
| {N7B5-Y7BB27SI-2946PUJK} | 01/02/2010 07:37:41 | MOH0273 | PC-6699 | Disconnect |
| {U1V9-Z7XT67KV-5649MYHI} | 01/02/2010 07:59:11 | HPH0075 | PC-2417 | Connect |
| {H0Z7-E6GB57XZ-1603MOXD} | 01/02/2010 07:59:49 | IIW0249 | PC-0843 | Connect |
| {L7P2-G4PX02RX-7999GYOY} | 01/02/2010 08:04:26 | IIW0249 | PC-0843 | Disconnect |

## File
- **Archivo:** `file.csv`
- **Tamaño aprox:** `184.11 MB`

### Esquema
| Columna | Tipo de Dato (Pandas) |
|---------|-----------------------|
| `id` | `str` |
| `date` | `str` |
| `user` | `str` |
| `pc` | `str` |
| `filename` | `str` |
| `content` | `str` |

### Muestra (primeras 5 filas)
| id | date | user | pc | filename | content |
| --- | --- | --- | --- | --- | --- |
| {L9G8-J9QE34VM-2834VDPB} | 01/02/2010 07:23:14 | MOH0273 | PC-6699 | EYPC9Y08.doc | D0-CF-11-E0-A1-B1-1A-E1 during difficulty overall cannons nonexistent threw authors leadership by rather under upper william an tip few savage expedition survey again trumbull could veteran too clearly single peak away own praise them snapped vessels against all toward |
| {H0W6-L4FG38XG-9897XTEN} | 01/02/2010 07:26:19 | MOH0273 | PC-6699 | N3LTSU3O.pdf | 25-50-44-46-2D carpenters 25 landed strait display channel boats difficulty august 14 south plattsburgh dc effusive earnest roads added find prevent march nonexistent first large strait garage recently strait leading a about young discovery manage navigable draw paid 48 england four run negotiating pushing inferior 8 inferior finally finally used drew mass howe 200 74 it charge cause all advanced world |
| {M3Z0-O2KK89OX-5716MBIM} | 01/02/2010 08:12:03 | HPH0075 | PC-2417 | D3D3WC9W.doc | D0-CF-11-E0-A1-B1-1A-E1 union 24 declined imposed brain employee 21 low action deadlines rear excitement preference toward bullet frank analysis 393 went march hear again floor subdued supreme about do yes up bay ever |
| {E1I4-S4QS61TG-3652YHKR} | 01/02/2010 08:17:00 | HPH0075 | PC-2417 | QCSW62YS.doc | D0-CF-11-E0-A1-B1-1A-E1 becoming period begin general much 1989 earlier black colleagues november 2011 used before him because conflict left concerned directions ignores wrist include executive mandate 50 over washington alternative nomination returned who developed dont king clearing martin began luther any good whisper deceased superior interview lined examination networks encountered individuals 1963 captured often suffered until image year radio maritime 8 patricks maintained twenty |
| {D4R7-E7JL45UX-0067XALT} | 01/02/2010 08:24:57 | HSB0196 | PC-8001 | AU75JV6U.jpg | FF-D8 |

## HTTP
- **Archivo:** `http.csv`
- **Tamaño aprox:** `13862.86 MB`

### Esquema
| Columna | Tipo de Dato (Pandas) |
|---------|-----------------------|
| `id` | `str` |
| `date` | `str` |
| `user` | `str` |
| `pc` | `str` |
| `url` | `str` |
| `content` | `str` |

### Muestra (primeras 5 filas)
| id | date | user | pc | url | content |
| --- | --- | --- | --- | --- | --- |
| {V1Y4-S2IR20QU-6154HFXJ} | 01/02/2010 06:55:16 | LRR0148 | PC-4275 | http://msn.com/The_Human_Centipede_First_Sequence/katsuro/arjf309875127.htm | remain representatives consensus concert although connect component collaborated mind sea 200 decision mixture regarding days warners rich fifth 1991 return 1988 apologized united crew tension particular allied rhythm making japanese enhance pop myself whole allmusic bras at focused throughout another touches want references |
| {Q5R1-T3EF87UE-2395RWZS} | 01/02/2010 07:00:13 | NGF0157 | PC-6056 | http://urbanspoon.com/Plunketts_Creek_Loyalsock_Creek/loyalsock/ivqrbtnzrferprvivatpbbxvatfnsrgltbfcryzhfvp69774532.jsp | festival off northwards than congestion partnership married 1830 acquired gentleman closely 17 take 1841 hundreds indicated allowing order characters disjunct hub temperature examples expanded adapted tribute |
| {X9O1-O0XW52VO-5806RPHG} | 01/02/2010 07:03:46 | NGF0157 | PC-6056 | http://aa.com/Rhodocene/rhodocenium/fhaavatqrfxgbcrkrphgvir1766627142.html | long away reorganized baldwin seth business 1888 while trail auction took joseph legislative prohibiting 4000 within heirs incorporated commerce years five length accepted researchers relatively del rearing authorities secondary energetic walls single |
| {G5S8-U5OG04TE-5299CCTU} | 01/02/2010 07:05:26 | IRM0931 | PC-7188 | http://groupon.com/Leonhard_Euler/leonhard/tneqravafrpgfsvfuvatobng292602446.php | among german schwein experimental becomes previously at above periods nitric then pushes such 6 felt treatment been christian known might found last local upon sweden animated been repeated presented from dress generally determine ninety robert off tossing should early from little easy |
| {L0R4-A9DH29VP-4553AUWM} | 01/02/2010 07:05:52 | IRM0931 | PC-7188 | http://flickr.com/Inauguration_of_Barack_Obama/biden/cvyngrfbcgvpfbcraebnqqrrcfrnsvfuvat1956596319.jsp | kate criteria j 2008 highest 12 include books ensuring recognize bef union trainers maps brought driven enfilading road thrust told agreement 1960 97 also expected ankle offer due 17th neither can |

## Email
- **Archivo:** `email.csv`
- **Tamaño aprox:** `1299.00 MB`

### Esquema
| Columna | Tipo de Dato (Pandas) |
|---------|-----------------------|
| `id` | `str` |
| `date` | `str` |
| `user` | `str` |
| `pc` | `str` |
| `to` | `str` |
| `cc` | `str` |
| `bcc` | `str` |
| `from` | `str` |
| `size` | `int64` |
| `attachments` | `int64` |
| `content` | `str` |

### Muestra (primeras 5 filas)
| id | date | user | pc | to | cc | bcc | from | size | attachments | content |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {R3I7-S4TX96FG-8219JWFF} | 01/02/2010 07:11:45 | LAP0338 | PC-5758 | Dean.Flynn.Hines@dtaa.com;Wade_Harrison@lockheedmartin.com | Nathaniel.Hunter.Heath@dtaa.com | nan | Lynn.Adena.Pratt@dtaa.com | 25830 | 0 | middle f2 systems 4 july techniques powerful destroyed who larger speeds plains part paul hold like followed over decrease actual training international addition geographically side able 34 29 such some appear prairies still 2009 succession yet 23 months mid america could most especially 34 off descend 2010 thus officially southward slope pass finland needed 2009 gulf stick possibility hall 49 montreal kick gulf |
| {R0R9-E4GL59IK-2907OSWJ} | 01/02/2010 07:12:16 | MOH0273 | PC-6699 | Odonnell-Gage@bellsouth.net | nan | nan | MOH68@optonline.net | 29942 | 0 | the breaking called allied reservations former further victories casualties one 18 douglas well sea until difficulty slopes coast message sailed remaining baltic awarded service sending restoration along z33 fjord village experience status cross entrance crashed review midnight up wearing eat glass six own |
| {G2B2-A8XY58CP-2847ZJZL} | 01/02/2010 07:13:00 | LAP0338 | PC-5758 | Penelope_Colon@netzero.com | nan | nan | Lynn_A_Pratt@earthlink.net | 28780 | 0 | slowly this uncinus winter beneath addition exist powered circumhorizontal contain one seasonally off glenn make addition lowered spot visible trigger 37 tails slowly two typically within dissipates then via researchers for 2008 like neptune wind he york entirely located contain |
| {A3A9-F4TH89AA-8318GFGK} | 01/02/2010 07:13:17 | LAP0338 | PC-5758 | Judith_Hayden@comcast.net | nan | nan | Lynn_A_Pratt@earthlink.net | 21907 | 0 | 400 other difficult land cirrocumulus powered probably especially for 37 humidity take conditions has gas bearing word cirrocumulus cirrostratus make deteriorate book edge satellite change regular great temperature before volume tiny college cover or castellanus are balance trail morning continues dissipates see such left one known sage bearing horizontally |
| {E8B7-C8FZ88UF-2946RUQQ} | 01/02/2010 07:13:28 | MOH0273 | PC-6699 | Bond-Raymond@verizon.net;Alea_Ferrell@msn.com;Jane_Mcdonald@juno.com | nan | Odonnell-Gage@bellsouth.net | MOH68@optonline.net | 17319 | 0 | this kmh october holliswood number advised unusually crew have amidst if succession fresh recorded continued and and deteriorated near between attracting down salomon 5th buried riches times embroidered days catholicism first sign against up aware airport merchant many conducted 9 dedicated bristol response spot following either suffered wholly closure spiritual |

## Psychometric
- **Archivo:** `psychometric.csv`
- **Tamaño aprox:** `0.04 MB`

### Esquema
| Columna | Tipo de Dato (Pandas) |
|---------|-----------------------|
| `employee_name` | `str` |
| `user_id` | `str` |
| `O` | `int64` |
| `C` | `int64` |
| `E` | `int64` |
| `A` | `int64` |
| `N` | `int64` |

### Muestra (primeras 5 filas)
| employee_name | user_id | O | C | E | A | N |
| --- | --- | --- | --- | --- | --- | --- |
| Calvin Edan Love | CEL0561 | 40 | 39 | 36 | 19 | 40 |
| Christine Reagan Deleon | CRD0624 | 26 | 22 | 17 | 39 | 32 |
| Jade Felicia Caldwell | JFC0557 | 22 | 16 | 23 | 40 | 33 |
| Aquila Stewart Dejesus | ASD0577 | 40 | 48 | 36 | 14 | 37 |
| Micah Abdul Rojas | MAR0955 | 36 | 44 | 23 | 44 | 25 |

## LDAP (Ejemplo: 2009-12)
- **Archivo:** `LDAP/2009-12.csv`
- **Tamaño aprox:** `0.14 MB`

### Esquema
| Columna | Tipo de Dato (Pandas) |
|---------|-----------------------|
| `employee_name` | `str` |
| `user_id` | `str` |
| `email` | `str` |
| `role` | `str` |
| `business_unit` | `int64` |
| `functional_unit` | `str` |
| `department` | `str` |
| `team` | `str` |
| `supervisor` | `str` |

### Muestra (primeras 5 filas)
| employee_name | user_id | email | role | business_unit | functional_unit | department | team | supervisor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Calvin Edan Love | CEL0561 | Calvin.Edan.Love@dtaa.com | ComputerProgrammer | 1 | 2 - ResearchAndEngineering | 2 - SoftwareManagement | 3 - Software | Stephanie Briar Harrington |
| Christine Reagan Deleon | CRD0624 | Christine.Reagan.Deleon@dtaa.com | Salesman | 1 | 5 - SalesAndMarketing | 2 - Sales | 3 - RegionalSales | Winter Veda Burks |
| Jade Felicia Caldwell | JFC0557 | Jade.Felicia.Caldwell@dtaa.com | SoftwareEngineer | 1 | 2 - ResearchAndEngineering | 2 - SoftwareManagement | 3 - Software | Stephanie Briar Harrington |
| Aquila Stewart Dejesus | ASD0577 | Aquila.Stewart.Dejesus@dtaa.com | ProductionLineWorker | 1 | 3 - Manufacturing | 3 - Assembly | 3 - AssemblyDept | Whilemina Pandora England |
| Micah Abdul Rojas | MAR0955 | Micah.Abdul.Rojas@dtaa.com | ProductionLineWorker | 1 | 3 - Manufacturing | 3 - Assembly | 6 - AssemblyDept | Sandra Beverly Diaz |

