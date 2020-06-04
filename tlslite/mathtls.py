# Authors: 
#   Trevor Perrin
#   Dave Baggett (Arcode Corporation) - MD5 support for MAC_SSL
#   Yngve Pettersen (ported by Paul Sokolovsky) - TLS 1.2
#   Hubert Kario - SHA384 PRF
#
# See the LICENSE file for legal information regarding use of this file.

"""Miscellaneous helper functions."""

from .utils.compat import *
from .utils.cryptomath import *
from .constants import CipherSuite
from .utils import tlshashlib as hashlib
from .utils import tlshmac as hmac
from .utils.deprecations import deprecated_method


# 1024, 1536, 2048, 3072, 4096, 6144, and 8192 bit groups from RFC 5054
# Formatted as in the RFC
goodGroupParameters = [
    # RFC 5054, 1, 1024-bit Group
    (2, int(remove_whitespace(
        """
          EEAF0AB9 ADB38DD6 9C33F80A FA8FC5E8 60726187 75FF3C0B 9EA2314C
          9C256576 D674DF74 96EA81D3 383B4813 D692C6E0 E0D5D8E2 50B98BE4
          8E495C1D 6089DAD1 5DC7D7B4 6154D6B6 CE8EF4AD 69B15D49 82559B29
          7BCF1885 C529F566 660E57EC 68EDBC3C 05726CC0 2FD4CBF4 976EAA9A
          FD5138FE 8376435B 9FC61D2F C0EB06E3"""), 16)),
    # RFC 5054, 2, 1536-bit Group
    (2, int(remove_whitespace(
        """
          9DEF3CAF B939277A B1F12A86 17A47BBB DBA51DF4 99AC4C80 BEEEA961
          4B19CC4D 5F4F5F55 6E27CBDE 51C6A94B E4607A29 1558903B A0D0F843
          80B655BB 9A22E8DC DF028A7C EC67F0D0 8134B1C8 B9798914 9B609E0B
          E3BAB63D 47548381 DBC5B1FC 764E3F4B 53DD9DA1 158BFD3E 2B9C8CF5
          6EDF0195 39349627 DB2FD53D 24B7C486 65772E43 7D6C7F8C E442734A
          F7CCB7AE 837C264A E3A9BEB8 7F8A2FE9 B8B5292E 5A021FFF 5E91479E
          8CE7A28C 2442C6F3 15180F93 499A234D CF76E3FE D135F9BB"""), 16)),
    # RFC 5054, 3, 2048-bit Group
    (2, int(remove_whitespace(
        """
          AC6BDB41 324A9A9B F166DE5E 1389582F AF72B665 1987EE07 FC319294
          3DB56050 A37329CB B4A099ED 8193E075 7767A13D D52312AB 4B03310D
          CD7F48A9 DA04FD50 E8083969 EDB767B0 CF609517 9A163AB3 661A05FB
          D5FAAAE8 2918A996 2F0B93B8 55F97993 EC975EEA A80D740A DBF4FF74
          7359D041 D5C33EA7 1D281E44 6B14773B CA97B43A 23FB8016 76BD207A
          436C6481 F1D2B907 8717461A 5B9D32E6 88F87748 544523B5 24B0D57D
          5EA77A27 75D2ECFA 032CFBDB F52FB378 61602790 04E57AE6 AF874E73
          03CE5329 9CCC041C 7BC308D8 2A5698F3 A8D0C382 71AE35F8 E9DBFBB6
          94B5C803 D89F7AE4 35DE236D 525F5475 9B65E372 FCD68EF2 0FA7111F
          9E4AFF73"""), 16)),
    # RFC 5054, 4, 3072-bit Group
    (5, int(remove_whitespace(
        """
          FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1 29024E08
          8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD EF9519B3 CD3A431B
          302B0A6D F25F1437 4FE1356D 6D51C245 E485B576 625E7EC6 F44C42E9
          A637ED6B 0BFF5CB6 F406B7ED EE386BFB 5A899FA5 AE9F2411 7C4B1FE6
          49286651 ECE45B3D C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8
          FD24CF5F 83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
          670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B E39E772C
          180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9 DE2BCBF6 95581718
          3995497C EA956AE5 15D22618 98FA0510 15728E5A 8AAAC42D AD33170D
          04507A33 A85521AB DF1CBA64 ECFB8504 58DBEF0A 8AEA7157 5D060C7D
          B3970F85 A6E1E4C7 ABF5AE8C DB0933D7 1E8C94E0 4A25619D CEE3D226
          1AD2EE6B F12FFA06 D98A0864 D8760273 3EC86A64 521F2B18 177B200C
          BBE11757 7A615D6C 770988C0 BAD946E2 08E24FA0 74E5AB31 43DB5BFC
          E0FD108E 4B82D120 A93AD2CA FFFFFFFF FFFFFFFF"""), 16)),
    # RFC 5054, 5, 4096-bit Group
    (5, int(remove_whitespace(
        """
          FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1 29024E08
          8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD EF9519B3 CD3A431B
          302B0A6D F25F1437 4FE1356D 6D51C245 E485B576 625E7EC6 F44C42E9
          A637ED6B 0BFF5CB6 F406B7ED EE386BFB 5A899FA5 AE9F2411 7C4B1FE6
          49286651 ECE45B3D C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8
          FD24CF5F 83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
          670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B E39E772C
          180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9 DE2BCBF6 95581718
          3995497C EA956AE5 15D22618 98FA0510 15728E5A 8AAAC42D AD33170D
          04507A33 A85521AB DF1CBA64 ECFB8504 58DBEF0A 8AEA7157 5D060C7D
          B3970F85 A6E1E4C7 ABF5AE8C DB0933D7 1E8C94E0 4A25619D CEE3D226
          1AD2EE6B F12FFA06 D98A0864 D8760273 3EC86A64 521F2B18 177B200C
          BBE11757 7A615D6C 770988C0 BAD946E2 08E24FA0 74E5AB31 43DB5BFC
          E0FD108E 4B82D120 A9210801 1A723C12 A787E6D7 88719A10 BDBA5B26
          99C32718 6AF4E23C 1A946834 B6150BDA 2583E9CA 2AD44CE8 DBBBC2DB
          04DE8EF9 2E8EFC14 1FBECAA6 287C5947 4E6BC05D 99B2964F A090C3A2
          233BA186 515BE7ED 1F612970 CEE2D7AF B81BDD76 2170481C D0069127
          D5B05AA9 93B4EA98 8D8FDDC1 86FFB7DC 90A6C08F 4DF435C9 34063199
          FFFFFFFF FFFFFFFF"""), 16)),
    # RFC 5054, 6, 6144-bit Group
    (5, int(remove_whitespace(
        """
          FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1 29024E08
          8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD EF9519B3 CD3A431B
          302B0A6D F25F1437 4FE1356D 6D51C245 E485B576 625E7EC6 F44C42E9
          A637ED6B 0BFF5CB6 F406B7ED EE386BFB 5A899FA5 AE9F2411 7C4B1FE6
          49286651 ECE45B3D C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8
          FD24CF5F 83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
          670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B E39E772C
          180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9 DE2BCBF6 95581718
          3995497C EA956AE5 15D22618 98FA0510 15728E5A 8AAAC42D AD33170D
          04507A33 A85521AB DF1CBA64 ECFB8504 58DBEF0A 8AEA7157 5D060C7D
          B3970F85 A6E1E4C7 ABF5AE8C DB0933D7 1E8C94E0 4A25619D CEE3D226
          1AD2EE6B F12FFA06 D98A0864 D8760273 3EC86A64 521F2B18 177B200C
          BBE11757 7A615D6C 770988C0 BAD946E2 08E24FA0 74E5AB31 43DB5BFC
          E0FD108E 4B82D120 A9210801 1A723C12 A787E6D7 88719A10 BDBA5B26
          99C32718 6AF4E23C 1A946834 B6150BDA 2583E9CA 2AD44CE8 DBBBC2DB
          04DE8EF9 2E8EFC14 1FBECAA6 287C5947 4E6BC05D 99B2964F A090C3A2
          233BA186 515BE7ED 1F612970 CEE2D7AF B81BDD76 2170481C D0069127
          D5B05AA9 93B4EA98 8D8FDDC1 86FFB7DC 90A6C08F 4DF435C9 34028492
          36C3FAB4 D27C7026 C1D4DCB2 602646DE C9751E76 3DBA37BD F8FF9406
          AD9E530E E5DB382F 413001AE B06A53ED 9027D831 179727B0 865A8918
          DA3EDBEB CF9B14ED 44CE6CBA CED4BB1B DB7F1447 E6CC254B 33205151
          2BD7AF42 6FB8F401 378CD2BF 5983CA01 C64B92EC F032EA15 D1721D03
          F482D7CE 6E74FEF6 D55E702F 46980C82 B5A84031 900B1C9E 59E7C97F
          BEC7E8F3 23A97A7E 36CC88BE 0F1D45B7 FF585AC5 4BD407B2 2B4154AA
          CC8F6D7E BF48E1D8 14CC5ED2 0F8037E0 A79715EE F29BE328 06A1D58B
          B7C5DA76 F550AA3D 8A1FBFF0 EB19CCB1 A313D55C DA56C9EC 2EF29632
          387FE8D7 6E3C0468 043E8F66 3F4860EE 12BF2D5B 0B7474D6 E694F91E
          6DCC4024 FFFFFFFF FFFFFFFF"""), 16)),
    # RFC 5054, 7, 8192-bit Group
    (19, int(remove_whitespace(
        """
          FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1 29024E08
          8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD EF9519B3 CD3A431B
          302B0A6D F25F1437 4FE1356D 6D51C245 E485B576 625E7EC6 F44C42E9
          A637ED6B 0BFF5CB6 F406B7ED EE386BFB 5A899FA5 AE9F2411 7C4B1FE6
          49286651 ECE45B3D C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8
          FD24CF5F 83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
          670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B E39E772C
          180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9 DE2BCBF6 95581718
          3995497C EA956AE5 15D22618 98FA0510 15728E5A 8AAAC42D AD33170D
          04507A33 A85521AB DF1CBA64 ECFB8504 58DBEF0A 8AEA7157 5D060C7D
          B3970F85 A6E1E4C7 ABF5AE8C DB0933D7 1E8C94E0 4A25619D CEE3D226
          1AD2EE6B F12FFA06 D98A0864 D8760273 3EC86A64 521F2B18 177B200C
          BBE11757 7A615D6C 770988C0 BAD946E2 08E24FA0 74E5AB31 43DB5BFC
          E0FD108E 4B82D120 A9210801 1A723C12 A787E6D7 88719A10 BDBA5B26
          99C32718 6AF4E23C 1A946834 B6150BDA 2583E9CA 2AD44CE8 DBBBC2DB
          04DE8EF9 2E8EFC14 1FBECAA6 287C5947 4E6BC05D 99B2964F A090C3A2
          233BA186 515BE7ED 1F612970 CEE2D7AF B81BDD76 2170481C D0069127
          D5B05AA9 93B4EA98 8D8FDDC1 86FFB7DC 90A6C08F 4DF435C9 34028492
          36C3FAB4 D27C7026 C1D4DCB2 602646DE C9751E76 3DBA37BD F8FF9406
          AD9E530E E5DB382F 413001AE B06A53ED 9027D831 179727B0 865A8918
          DA3EDBEB CF9B14ED 44CE6CBA CED4BB1B DB7F1447 E6CC254B 33205151
          2BD7AF42 6FB8F401 378CD2BF 5983CA01 C64B92EC F032EA15 D1721D03
          F482D7CE 6E74FEF6 D55E702F 46980C82 B5A84031 900B1C9E 59E7C97F
          BEC7E8F3 23A97A7E 36CC88BE 0F1D45B7 FF585AC5 4BD407B2 2B4154AA
          CC8F6D7E BF48E1D8 14CC5ED2 0F8037E0 A79715EE F29BE328 06A1D58B
          B7C5DA76 F550AA3D 8A1FBFF0 EB19CCB1 A313D55C DA56C9EC 2EF29632
          387FE8D7 6E3C0468 043E8F66 3F4860EE 12BF2D5B 0B7474D6 E694F91E
          6DBE1159 74A3926F 12FEE5E4 38777CB6 A932DF8C D8BEC4D0 73B931BA
          3BC832B6 8D9DD300 741FA7BF 8AFC47ED 2576F693 6BA42466 3AAB639C
          5AE4F568 3423B474 2BF1C978 238F16CB E39D652D E3FDB8BE FC848AD9
          22222E04 A4037C07 13EB57A8 1A23F0C7 3473FC64 6CEA306B 4BCBC886
          2F8385DD FA9D4B7F A2C087E8 79683303 ED5BDD3A 062B3CF5 B3A278A6
          6D2A13F8 3F44F82D DF310EE0 74AB6A36 4597E899 A0255DC1 64F31CC5
          0846851D F9AB4819 5DED7EA1 B1D510BD 7EE74D73 FAF36BC3 1ECFA268
          359046F4 EB879F92 4009438B 481C6CD7 889A002E D5EE382B C9190DA6
          FC026E47 9558E447 5677E9AA 9E3050E2 765694DF C81F56E8 80B96E71
          60C980DD 98EDD3DF FFFFFFFF FFFFFFFF"""), 16))]


# old versions of tlslite had an incorrect generator for 3072 bit group
# from RFC 5054. Since the group is a safe prime, the generator of "2" is
# cryptographically safe, so we don't have reason to reject connections
# from old tlslite, so add the old invalid value to the "known good" list
goodGroupParameters.append((2, goodGroupParameters[3][1]))
# we had a bad generator for group 7 (8192 bit) - 5 - while it needs to be 19
# same as above, any generator but 1 and p-1 are ok, cryptographically speaking
goodGroupParameters.append((5, goodGroupParameters[6][1]))

RFC7919_GROUPS = []

# RFC 7919 ffdhe2048 bit group
FFDHE2048 = (2,
             int("FFFFFFFFFFFFFFFFADF85458A2BB4A9AAFDC5620273D3CF1"
                 "D8B9C583CE2D3695A9E13641146433FBCC939DCE249B3EF9"
                 "7D2FE363630C75D8F681B202AEC4617AD3DF1ED5D5FD6561"
                 "2433F51F5F066ED0856365553DED1AF3B557135E7F57C935"
                 "984F0C70E0E68B77E2A689DAF3EFE8721DF158A136ADE735"
                 "30ACCA4F483A797ABC0AB182B324FB61D108A94BB2C8E3FB"
                 "B96ADAB760D7F4681D4F42A3DE394DF4AE56EDE76372BB19"
                 "0B07A7C8EE0A6D709E02FCE1CDF7E2ECC03404CD28342F61"
                 "9172FE9CE98583FF8E4F1232EEF28183C3FE3B1B4C6FAD73"
                 "3BB5FCBC2EC22005C58EF1837D1683B2C6F34A26C1B2EFFA"
                 "886B423861285C97FFFFFFFFFFFFFFFF", 16))
goodGroupParameters.append(FFDHE2048)
RFC7919_GROUPS.append(FFDHE2048)

# RFC 7919 ffdhe3072 bit group
FFDHE3072 = (2,
             int("FFFFFFFFFFFFFFFFADF85458A2BB4A9AAFDC5620273D3CF1"
                 "D8B9C583CE2D3695A9E13641146433FBCC939DCE249B3EF9"
                 "7D2FE363630C75D8F681B202AEC4617AD3DF1ED5D5FD6561"
                 "2433F51F5F066ED0856365553DED1AF3B557135E7F57C935"
                 "984F0C70E0E68B77E2A689DAF3EFE8721DF158A136ADE735"
                 "30ACCA4F483A797ABC0AB182B324FB61D108A94BB2C8E3FB"
                 "B96ADAB760D7F4681D4F42A3DE394DF4AE56EDE76372BB19"
                 "0B07A7C8EE0A6D709E02FCE1CDF7E2ECC03404CD28342F61"
                 "9172FE9CE98583FF8E4F1232EEF28183C3FE3B1B4C6FAD73"
                 "3BB5FCBC2EC22005C58EF1837D1683B2C6F34A26C1B2EFFA"
                 "886B4238611FCFDCDE355B3B6519035BBC34F4DEF99C0238"
                 "61B46FC9D6E6C9077AD91D2691F7F7EE598CB0FAC186D91C"
                 "AEFE130985139270B4130C93BC437944F4FD4452E2D74DD3"
                 "64F2E21E71F54BFF5CAE82AB9C9DF69EE86D2BC522363A0D"
                 "ABC521979B0DEADA1DBF9A42D5C4484E0ABCD06BFA53DDEF"
                 "3C1B20EE3FD59D7C25E41D2B66C62E37FFFFFFFFFFFFFFFF", 16))
goodGroupParameters.append(FFDHE3072)
RFC7919_GROUPS.append(FFDHE3072)

# RFC 7919 ffdhe4096 bit group
FFDHE4096 = (2,
             int("FFFFFFFFFFFFFFFFADF85458A2BB4A9AAFDC5620273D3CF1"
                 "D8B9C583CE2D3695A9E13641146433FBCC939DCE249B3EF9"
                 "7D2FE363630C75D8F681B202AEC4617AD3DF1ED5D5FD6561"
                 "2433F51F5F066ED0856365553DED1AF3B557135E7F57C935"
                 "984F0C70E0E68B77E2A689DAF3EFE8721DF158A136ADE735"
                 "30ACCA4F483A797ABC0AB182B324FB61D108A94BB2C8E3FB"
                 "B96ADAB760D7F4681D4F42A3DE394DF4AE56EDE76372BB19"
                 "0B07A7C8EE0A6D709E02FCE1CDF7E2ECC03404CD28342F61"
                 "9172FE9CE98583FF8E4F1232EEF28183C3FE3B1B4C6FAD73"
                 "3BB5FCBC2EC22005C58EF1837D1683B2C6F34A26C1B2EFFA"
                 "886B4238611FCFDCDE355B3B6519035BBC34F4DEF99C0238"
                 "61B46FC9D6E6C9077AD91D2691F7F7EE598CB0FAC186D91C"
                 "AEFE130985139270B4130C93BC437944F4FD4452E2D74DD3"
                 "64F2E21E71F54BFF5CAE82AB9C9DF69EE86D2BC522363A0D"
                 "ABC521979B0DEADA1DBF9A42D5C4484E0ABCD06BFA53DDEF"
                 "3C1B20EE3FD59D7C25E41D2B669E1EF16E6F52C3164DF4FB"
                 "7930E9E4E58857B6AC7D5F42D69F6D187763CF1D55034004"
                 "87F55BA57E31CC7A7135C886EFB4318AED6A1E012D9E6832"
                 "A907600A918130C46DC778F971AD0038092999A333CB8B7A"
                 "1A1DB93D7140003C2A4ECEA9F98D0ACC0A8291CDCEC97DCF"
                 "8EC9B55A7F88A46B4DB5A851F44182E1C68A007E5E655F6A"
                 "FFFFFFFFFFFFFFFF", 16))
goodGroupParameters.append(FFDHE4096)
RFC7919_GROUPS.append(FFDHE4096)

# RFC 7919 ffdhe6144 bit group
FFDHE6144 = (2,
             int("FFFFFFFFFFFFFFFFADF85458A2BB4A9AAFDC5620273D3CF1"
                 "D8B9C583CE2D3695A9E13641146433FBCC939DCE249B3EF9"
                 "7D2FE363630C75D8F681B202AEC4617AD3DF1ED5D5FD6561"
                 "2433F51F5F066ED0856365553DED1AF3B557135E7F57C935"
                 "984F0C70E0E68B77E2A689DAF3EFE8721DF158A136ADE735"
                 "30ACCA4F483A797ABC0AB182B324FB61D108A94BB2C8E3FB"
                 "B96ADAB760D7F4681D4F42A3DE394DF4AE56EDE76372BB19"
                 "0B07A7C8EE0A6D709E02FCE1CDF7E2ECC03404CD28342F61"
                 "9172FE9CE98583FF8E4F1232EEF28183C3FE3B1B4C6FAD73"
                 "3BB5FCBC2EC22005C58EF1837D1683B2C6F34A26C1B2EFFA"
                 "886B4238611FCFDCDE355B3B6519035BBC34F4DEF99C0238"
                 "61B46FC9D6E6C9077AD91D2691F7F7EE598CB0FAC186D91C"
                 "AEFE130985139270B4130C93BC437944F4FD4452E2D74DD3"
                 "64F2E21E71F54BFF5CAE82AB9C9DF69EE86D2BC522363A0D"
                 "ABC521979B0DEADA1DBF9A42D5C4484E0ABCD06BFA53DDEF"
                 "3C1B20EE3FD59D7C25E41D2B669E1EF16E6F52C3164DF4FB"
                 "7930E9E4E58857B6AC7D5F42D69F6D187763CF1D55034004"
                 "87F55BA57E31CC7A7135C886EFB4318AED6A1E012D9E6832"
                 "A907600A918130C46DC778F971AD0038092999A333CB8B7A"
                 "1A1DB93D7140003C2A4ECEA9F98D0ACC0A8291CDCEC97DCF"
                 "8EC9B55A7F88A46B4DB5A851F44182E1C68A007E5E0DD902"
                 "0BFD64B645036C7A4E677D2C38532A3A23BA4442CAF53EA6"
                 "3BB454329B7624C8917BDD64B1C0FD4CB38E8C334C701C3A"
                 "CDAD0657FCCFEC719B1F5C3E4E46041F388147FB4CFDB477"
                 "A52471F7A9A96910B855322EDB6340D8A00EF092350511E3"
                 "0ABEC1FFF9E3A26E7FB29F8C183023C3587E38DA0077D9B4"
                 "763E4E4B94B2BBC194C6651E77CAF992EEAAC0232A281BF6"
                 "B3A739C1226116820AE8DB5847A67CBEF9C9091B462D538C"
                 "D72B03746AE77F5E62292C311562A846505DC82DB854338A"
                 "E49F5235C95B91178CCF2DD5CACEF403EC9D1810C6272B04"
                 "5B3B71F9DC6B80D63FDD4A8E9ADB1E6962A69526D43161C1"
                 "A41D570D7938DAD4A40E329CD0E40E65FFFFFFFFFFFFFFFF", 16))
goodGroupParameters.append(FFDHE6144)
RFC7919_GROUPS.append(FFDHE6144)

# RFC 7919 ffdhe8192 bit group
FFDHE8192 = (2,
             int("FFFFFFFFFFFFFFFFADF85458A2BB4A9AAFDC5620273D3CF1"
                 "D8B9C583CE2D3695A9E13641146433FBCC939DCE249B3EF9"
                 "7D2FE363630C75D8F681B202AEC4617AD3DF1ED5D5FD6561"
                 "2433F51F5F066ED0856365553DED1AF3B557135E7F57C935"
                 "984F0C70E0E68B77E2A689DAF3EFE8721DF158A136ADE735"
                 "30ACCA4F483A797ABC0AB182B324FB61D108A94BB2C8E3FB"
                 "B96ADAB760D7F4681D4F42A3DE394DF4AE56EDE76372BB19"
                 "0B07A7C8EE0A6D709E02FCE1CDF7E2ECC03404CD28342F61"
                 "9172FE9CE98583FF8E4F1232EEF28183C3FE3B1B4C6FAD73"
                 "3BB5FCBC2EC22005C58EF1837D1683B2C6F34A26C1B2EFFA"
                 "886B4238611FCFDCDE355B3B6519035BBC34F4DEF99C0238"
                 "61B46FC9D6E6C9077AD91D2691F7F7EE598CB0FAC186D91C"
                 "AEFE130985139270B4130C93BC437944F4FD4452E2D74DD3"
                 "64F2E21E71F54BFF5CAE82AB9C9DF69EE86D2BC522363A0D"
                 "ABC521979B0DEADA1DBF9A42D5C4484E0ABCD06BFA53DDEF"
                 "3C1B20EE3FD59D7C25E41D2B669E1EF16E6F52C3164DF4FB"
                 "7930E9E4E58857B6AC7D5F42D69F6D187763CF1D55034004"
                 "87F55BA57E31CC7A7135C886EFB4318AED6A1E012D9E6832"
                 "A907600A918130C46DC778F971AD0038092999A333CB8B7A"
                 "1A1DB93D7140003C2A4ECEA9F98D0ACC0A8291CDCEC97DCF"
                 "8EC9B55A7F88A46B4DB5A851F44182E1C68A007E5E0DD902"
                 "0BFD64B645036C7A4E677D2C38532A3A23BA4442CAF53EA6"
                 "3BB454329B7624C8917BDD64B1C0FD4CB38E8C334C701C3A"
                 "CDAD0657FCCFEC719B1F5C3E4E46041F388147FB4CFDB477"
                 "A52471F7A9A96910B855322EDB6340D8A00EF092350511E3"
                 "0ABEC1FFF9E3A26E7FB29F8C183023C3587E38DA0077D9B4"
                 "763E4E4B94B2BBC194C6651E77CAF992EEAAC0232A281BF6"
                 "B3A739C1226116820AE8DB5847A67CBEF9C9091B462D538C"
                 "D72B03746AE77F5E62292C311562A846505DC82DB854338A"
                 "E49F5235C95B91178CCF2DD5CACEF403EC9D1810C6272B04"
                 "5B3B71F9DC6B80D63FDD4A8E9ADB1E6962A69526D43161C1"
                 "A41D570D7938DAD4A40E329CCFF46AAA36AD004CF600C838"
                 "1E425A31D951AE64FDB23FCEC9509D43687FEB69EDD1CC5E"
                 "0B8CC3BDF64B10EF86B63142A3AB8829555B2F747C932665"
                 "CB2C0F1CC01BD70229388839D2AF05E454504AC78B758282"
                 "2846C0BA35C35F5C59160CC046FD8251541FC68C9C86B022"
                 "BB7099876A460E7451A8A93109703FEE1C217E6C3826E52C"
                 "51AA691E0E423CFC99E9E31650C1217B624816CDAD9A95F9"
                 "D5B8019488D9C0A0A1FE3075A577E23183F81D4A3F2FA457"
                 "1EFC8CE0BA8A4FE8B6855DFE72B0A66EDED2FBABFBE58A30"
                 "FAFABE1C5D71A87E2F741EF8C1FE86FEA6BBFDE530677F0D"
                 "97D11D49F7A8443D0822E506A9F4614E011E2A94838FF88C"
                 "D68C8BB7C5C6424CFFFFFFFFFFFFFFFF", 16))
goodGroupParameters.append(FFDHE8192)
RFC7919_GROUPS.append(FFDHE8192)


def paramStrength(param):
    """
    Return level of security for DH, DSA and RSA parameters.

    Provide the approximate level of security for algorithms based on finite
    field (DSA, DH) or integer factorisation cryptography (RSA) when provided
    with the prime defining the field or the modulus of the public key.

    :param param: prime or modulus
    :type param: int
    """
    size = numBits(param)
    if size < 512:
        return 48
    elif size < 768:
        return 56
    elif size < 816:
        return 64
    elif size < 1023:
        return 72
    elif size < 1535:
        return 80  # NIST SP 800-57
    elif size < 2047:
        return 88  # rounded RFC 3526
    elif size < 3071:
        return 112  # NIST SP 800-57
    elif size < 4095:
        return 128  # NIST SP 800-57
    elif size < 6144:
        return 152  # rounded RFC 3526
    elif size < 7679:
        return 168  # rounded RFC 3526
    elif size < 15359:
        return 192  # NIST SP 800-57
    else:
        return 256  # NIST SP 800-57


def P_hash(macFunc, secret, seed, length):
    bytes = bytearray(length)
    A = seed
    index = 0
    while 1:
        A = macFunc(secret, A)
        output = macFunc(secret, A + seed)
        for c in output:
            if index >= length:
                return bytes
            bytes[index] = c
            index += 1
    return bytes

def PRF(secret, label, seed, length):
    #Split the secret into left and right halves
    # which may share a byte if len is odd
    S1 = secret[ : int(math.ceil(len(secret)/2.0))]
    S2 = secret[ int(math.floor(len(secret)/2.0)) : ]

    #Run the left half through P_MD5 and the right half through P_SHA1
    p_md5 = P_hash(HMAC_MD5, S1, label + seed, length)
    p_sha1 = P_hash(HMAC_SHA1, S2, label + seed, length)

    #XOR the output values and return the result
    for x in range(length):
        p_md5[x] ^= p_sha1[x]
    return p_md5

def PRF_1_2(secret, label, seed, length):
    """Pseudo Random Function for TLS1.2 ciphers that use SHA256"""
    return P_hash(HMAC_SHA256, secret, label + seed, length)

def PRF_1_2_SHA384(secret, label, seed, length):
    """Pseudo Random Function for TLS1.2 ciphers that use SHA384"""
    return P_hash(HMAC_SHA384, secret, label + seed, length)

def PRF_SSL(secret, seed, length):
    bytes = bytearray(length)
    index = 0
    for x in range(26):
        A = bytearray([ord('A')+x] * (x+1)) # 'A', 'BB', 'CCC', etc..
        input = secret + SHA1(A + secret + seed)
        output = MD5(input)
        for c in output:
            if index >= length:
                return bytes
            bytes[index] = c
            index += 1
    return bytes

@deprecated_method("Please use calcKey method instead.")
def calcExtendedMasterSecret(version, cipherSuite, premasterSecret,
                             handshakeHashes):
    """Derive Extended Master Secret from premaster and handshake msgs"""
    assert version in ((3, 1), (3, 2), (3, 3))
    if version in ((3, 1), (3, 2)):
        masterSecret = PRF(premasterSecret, b"extended master secret",
                           handshakeHashes.digest('md5') +
                           handshakeHashes.digest('sha1'),
                           48)
    else:
        if cipherSuite in CipherSuite.sha384PrfSuites:
            masterSecret = PRF_1_2_SHA384(premasterSecret,
                                          b"extended master secret",
                                          handshakeHashes.digest('sha384'),
                                          48)
        else:
            masterSecret = PRF_1_2(premasterSecret,
                                   b"extended master secret",
                                   handshakeHashes.digest('sha256'),
                                   48)
    return masterSecret


@deprecated_method("Please use calcKey method instead.")
def calcMasterSecret(version, cipherSuite, premasterSecret, clientRandom,
                     serverRandom):
    """Derive Master Secret from premaster secret and random values"""
    if version == (3,0):
        masterSecret = PRF_SSL(premasterSecret,
                            clientRandom + serverRandom, 48)
    elif version in ((3,1), (3,2)):
        masterSecret = PRF(premasterSecret, b"master secret",
                            clientRandom + serverRandom, 48)
    elif version == (3,3):
        if cipherSuite in CipherSuite.sha384PrfSuites:
            masterSecret = PRF_1_2_SHA384(premasterSecret,
                                          b"master secret",
                                          clientRandom + serverRandom,
                                          48)
        else:
            masterSecret = PRF_1_2(premasterSecret,
                                   b"master secret",
                                   clientRandom + serverRandom,
                                   48)
    else:
        raise AssertionError()
    return masterSecret

@deprecated_method("Please use calcKey method instead.")
def calcFinished(version, masterSecret, cipherSuite, handshakeHashes,
                 isClient):
    """Calculate the Handshake protocol Finished value

    :param version: TLS protocol version tuple
    :param masterSecret: negotiated master secret of the connection
    :param cipherSuite: negotiated cipher suite of the connection,
    :param handshakeHashes: running hash of the handshake messages
    :param isClient: whether the calculation should be performed for message
        sent by client (True) or by server (False) side of connection
    """
    assert version in ((3, 0), (3, 1), (3, 2), (3, 3))
    if version == (3,0):
        if isClient:
            senderStr = b"\x43\x4C\x4E\x54"
        else:
            senderStr = b"\x53\x52\x56\x52"

        verifyData = handshakeHashes.digestSSL(masterSecret, senderStr)
    else:
        if isClient:
            label = b"client finished"
        else:
            label = b"server finished"

        if version in ((3,1), (3,2)):
            handshakeHash = handshakeHashes.digest()
            verifyData = PRF(masterSecret, label, handshakeHash, 12)
        else: # version == (3,3):
            if cipherSuite in CipherSuite.sha384PrfSuites:
                handshakeHash = handshakeHashes.digest('sha384')
                verifyData = PRF_1_2_SHA384(masterSecret, label,
                                            handshakeHash, 12)
            else:
                handshakeHash = handshakeHashes.digest('sha256')
                verifyData = PRF_1_2(masterSecret, label, handshakeHash, 12)

    return verifyData

def calc_key(version, secret, cipher_suite, label, handshake_hashes=None,
            client_random=None, server_random=None, output_length=None):
    """
    Method for calculating different keys depending on input.
    It can be used to calculate finished value, master secret,
    extended master secret or key expansion.

    :param version: TLS protocol version
    :type version: tuple(int, int)
    :param bytearray secret: master secret or premasterSecret which will be
        used in the PRF.
    :param int cipher_suite: Negotiated cipher suite of the connection.
    :param bytes label: label for the key you want to calculate
        (ex. 'master secret', 'extended master secret', etc).
    :param handshake_hashes: running hash of the handshake messages
        needed for calculating extended master secret or finished value.
    :type handshake_hashes: ~tlslite.handshakehashes.HandshakeHashes
    :param bytearray client_random: client random needed for calculating
        master secret or key expansion.
    :param bytearray server_random: server random needed for calculating
        master secret or key expansion.
    :param int output_length: Number of bytes to output.
    """


    # SSL3 calculations.
    if version == (3, 0):
        # Calculating Finished value, either for message sent
        # by server or by client
        if label == b"client finished":
            senderStr = b"\x43\x4C\x4E\x54"
            return handshake_hashes.digestSSL(secret, senderStr)
        elif label == b"server finished":
            senderStr = b"\x53\x52\x56\x52"
            return handshake_hashes.digestSSL(secret, senderStr)
        else:
            assert label in [b"key expansion", b"master secret"]
            func = PRF_SSL

    # TLS1.0 or TLS1.1 calculations.
    elif version in ((3, 1), (3, 2)):
        func = PRF
        # Seed needed for calculating extended master secret
        if label == b"extended master secret":
            seed = handshake_hashes.digest('md5') + \
                   handshake_hashes.digest('sha1')
        # Seed needed for calculating Finished value
        elif label in [b"server finished", b"client finished"]:
            seed = handshake_hashes.digest()
        else:
            assert label in [b"key expansion", b"master secret"]

    # TLS1.2 calculations.
    else:
        assert version == (3, 3)
        if cipher_suite in CipherSuite.sha384PrfSuites:
            func = PRF_1_2_SHA384
            # Seed needed for calculating Finished value or extended master
            # secret
            if label in [b"extended master secret", b"server finished",
                    b"client finished"]:
                seed = handshake_hashes.digest('sha384')
            else:
                assert label in [b"key expansion", b"master secret"]
        else:
            # Same as above, just using sha256
            func = PRF_1_2
            if label in [b"extended master secret", b"server finished",
                    b"client finished"]:
                seed = handshake_hashes.digest('sha256')
            else:
                assert label in [b"key expansion", b"master secret"]

    # Seed needed for calculating key expansion or master secret
    if label == b"key expansion":
        seed = server_random + client_random
    if label == b"master secret":
        seed = client_random + server_random

    if func == PRF_SSL:
        return func(secret, seed, output_length)
    return func(secret, label, seed, output_length)

def makeX(salt, username, password):
    if len(username)>=256:
        raise ValueError("username too long")
    if len(salt)>=256:
        raise ValueError("salt too long")
    innerHashResult = SHA1(username + bytearray(b":") + password)
    outerHashResult = SHA1(salt + innerHashResult)
    return bytesToNumber(outerHashResult)

#This function is used by VerifierDB.makeVerifier
def makeVerifier(username, password, bits):
    bitsIndex = {1024:0, 1536:1, 2048:2, 3072:3, 4096:4, 6144:5, 8192:6}[bits]
    g,N = goodGroupParameters[bitsIndex]
    salt = getRandomBytes(16)
    x = makeX(salt, username, password)
    verifier = powMod(g, x, N)
    return N, g, salt, verifier

def PAD(n, x):
    nLength = len(numberToByteArray(n))
    b = numberToByteArray(x)
    if len(b) < nLength:
        b = (b"\0" * (nLength-len(b))) + b
    return b

def makeU(N, A, B):
  return bytesToNumber(SHA1(PAD(N, A) + PAD(N, B)))

def makeK(N, g):
  return bytesToNumber(SHA1(numberToByteArray(N) + PAD(N, g)))

def createHMAC(k, digestmod=hashlib.sha1):
    h = hmac.HMAC(k, digestmod=digestmod)
    if not hasattr(h, 'block_size'):
        h.block_size = digestmod().block_size
    assert h.block_size == digestmod().block_size
    return h

def createMAC_SSL(k, digestmod=None):
    mac = MAC_SSL()
    mac.create(k, digestmod=digestmod)
    return mac


class MAC_SSL(object):
    def create(self, k, digestmod=None):
        self.digestmod = digestmod or hashlib.sha1
        self.block_size = self.digestmod().block_size
        # Repeat pad bytes 48 times for MD5; 40 times for other hash functions.
        self.digest_size = 16 if (self.digestmod is hashlib.md5) else 20
        repeat = 40 if self.digest_size == 20 else 48
        opad = b"\x5C" * repeat
        ipad = b"\x36" * repeat

        self.ohash = self.digestmod(k + opad)
        self.ihash = self.digestmod(k + ipad)

    def update(self, m):
        self.ihash.update(m)

    def copy(self):
        new = MAC_SSL()
        new.ihash = self.ihash.copy()
        new.ohash = self.ohash.copy()
        new.digestmod = self.digestmod
        new.digest_size = self.digest_size
        new.block_size = self.block_size
        return new

    def digest(self):
        ohash2 = self.ohash.copy()
        ohash2.update(self.ihash.digest())
        return bytearray(ohash2.digest())
