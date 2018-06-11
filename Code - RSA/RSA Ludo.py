from random import randint,choice
from time import perf_counter

# Données :

# Privées : p, q, d premier avec (p-1)*(q-1)=phi(p*q)
# Publiques : n=p*q, e tel que e*d=1 mod phi(n)

def pgcd(a,b): #algorithme d'Euclide
    while a%b!=0:
        a,b=b,a%b
    return b

def inversmod(a,p):
    '''a**(-1) mod p'''
    #algorithme d'euclide étendu (solution de l'equation de Bezout)
    r1,u1,v1,r2,u2,v2=a,1,0,p,0,1

    while r2!=0:
        q=r1//r2
        r1,u1,v1,r2,u2,v2=r2,u2,v2,r1-q*r2,u1-q*u2,v1-q*v2
    if r1!=1:
        return 'pas inversible'
    else:
        if u1<1:
            while u1<1:
                u1+=p
        if u1>p:
            while u1>p:
                u1-=p
        return u1

def puissmod(a,d,n):
    dbin=bin(d)
    L=[int(dbin[-i-1]) for i in range(len(dbin)-2)]
    res=1
    while L!=[]:
        k=L.pop(0)
        if k>0:
            res=res*a%n
        a=a**2%n
    return res

def MillerRabin_test(n,k): #primalité de n a tester et k nombre de boucles

    for t in range(k):
        a=randint(2,n-2)
        if MillerRabin_temoin(a,n):
            return False
    return True

def MillerRabin_temoin(a,n):
    #Calcul de s et d tels que n-1=2**s*d
    d=(n-1)//2
    s=1
    while d%2==0:
        d=d//2
        s+=1

    #Premier test
    x=puissmod(a,d,n)
    if x==1 or x==n-1 :
        return False

    #Boucle principale

    while s>1:
        x=x**2%n
        if x==n-1:
            return False
        s-=1

    return True

def MillerRabin_generation(b): #longueur en base 10 du nombre premier (proba pas premier 10**-30)
    i=0
    while True:
        i+=1
        n=choice([1,3,5,7,9]) #candidat premier
        for k in range(1,b-1) :
            n+=randint(0,9)*10**k
        n+=randint(1,9)*10**b
        if MillerRabin_test(n,100):
            return i,n

def generateur2(n):
    while True:
        q=MillerRabin_generation(n)[1]
        for k in range(1,500):
            p=k*q+1
            if MillerRabin_test(p,100):
                return p

def RSA_generation(n):
    p=generateur2(n)
    q=generateur2(n) #pas B friable
    phi=(p-1)*(q-1)
    d=randint(1,phi)
    while pgcd(phi,d)!=1:
        d=randint(1,phi)
    e=inversmod(d,phi)
    n=p*q
    return n,e,d

def test_RSA_generation(i,j,pas):
    for n in range(i,j,pas):
        T=[]
        for s in range(10):
            t1=perf_counter()
            RSA_generation(n)
            t2=perf_counter()
            T.append(t2-t1)
        print(n,sum(T)/10,sep=';')


def RSA_chiffrement(m,e,n):
    c=puissmod(m,e,n)
    return c

def RSA_dechiffrement(c,d,n):
    m=puissmod(c,d,n)
    return m

def RSA_signature(h,d,n):
    s=puissmod(h,d,n)
    return s

def RSA_verification(s,h,e,n):
    if puissmod(s,e,n)==h:
        return True
    else:
        return False







#Choix p et q à 200 chiffres

def test_RSA(i,j,pas): #taille du message en nombre de caractères
    '''taille;tchif;tdechif;tsign;tverif'''
    global N
    global E
    global D

    for k in range(i,j,pas):
        Tchif=[]
        Tdechif=[]
        Tsign=[]
        Tverif=[]
        for s in range(10):
            n,e,d=N[s],E[s],D[s]
            q=k//166
            r=k-q
            max=sum([2**pui for pui in range(8*r)])
            B_clair=[randint(1,n-1) for i in range(q)]+[randint(1,max)]
            tchif=0
            tdechif=0
            tsign=0
            tverif=0
            for bloc in B_clair:
                t1=perf_counter()
                c=RSA_chiffrement(bloc,d,n)
                t2=perf_counter()
                tchif+=t2-t1

                t1=perf_counter()
                s=RSA_signature(c,d,n)
                t2=perf_counter()
                tsign+=t2-t1

                t1=perf_counter()
                RSA_dechiffrement(c,d,n)
                t2=perf_counter()
                tdechif+=t2-t1

                t1=perf_counter()
                RSA_verification(s,c,e,n)
                t2=perf_counter()
                tverif+=t2-t1
            Tchif.append(tchif)
            Tdechif.append(tdechif)
            Tsign.append(tsign)
            Tverif.append(tverif)


        print(k,sum(Tchif)/10,sum(Tdechif)/10,sum(Tsign)/10,sum(Tverif)/10,sep=';')

N=[12452390767519337078726161200801221856474403991507345254673036824163742534476598126187031114930954227947839069585497073175254455516890066684459166184657874995192698321159190823278955942793403722678374118445753322506410911583899285111507540729694608096796578459024632393085615011203490574694004845733348438757782813094388723818676869349701809212755910602025312182402652283811287835369509156950865282732349883,
2453376466472741280511151506882620939640647727172558713663138276457572296043133970423148747242005309179733981055193419549498658726962751359907067390718558084511370948190311000927285815566817455512456291681165928443557620877479674854089403869933937101786758322931821588477664174445896650606584602175004970268997888640506148898914760599478329075012175525384906783636388503615676930055007609820798473719815013,
4954757752839323971702406527297656949152889693505112140309219393701927232947267936422367381617489521332849797703138751007419190235665927876469124489135744629014907205422443233032853131347626120816960288936993020966206555948229598768216523289797446491961561862848613748096193130419158702567769044290579886721718718228247414228554223332946756380720188129233771071679885226850794559741144671636492709129500389,
15687490519023357468274385562535182974995391974651251745411386587854070128892453692590442927943411894025412162141731077771606900719036054665501636294514893880060333984471114095878153977582056229595660491914969775264305686562292938548691140514380295490742352437035834856913540268747850084750416152792815063845982192648885706092709646878451563536462362934404574116537855957128075323191984739404177257965009873,
13074952170390083537868090581604739295435219766352338160969309032640565846816606368907175718817779831310413400883006576748026238006816286874647463658103559266176920237585646626114638058483259941201225605836611679688493526237893169942364742830116357258617160986513720293975489380843893830262803725934549525333090162444269529870384109798777770192464539902677988796921269605701771944857583484221140656808096483,
10232636223664571174497515289048339197633044872808023618486155721418966224334116745596121419343219208967937037595251948398641513226594817038190179233347095686403916959861003935659010979000394906151848395174522484607136463412385449330876654493608903390873928365136220605628977185943212565037532156059156623337300862493623694441556618590213799372290430260642488213284132522617139035582981835279874039745270017,
17969400172349127515015247626452734710698620870778216051794538659479065017297642016444705457566952907102196505804543416556312485751534668041241532035123519992217394961417176705447426988257176220857823922512441751123885847334517714336696801102114349521581127991682926592550576375671298688105728279810736184976418827662719609034041957016382546443598980044558224743753028386481615790657910802174009070916839,
6955757248511180452141992238152202881403109520270824142794597954420831138332542133102646805698210611573479270078267767815325159145327999790113874531140035012871467021690603348093964102741727662664757180392870981584361204824740725643855536053592630820779987167091508684125132041523337717850674223041040156083729761332378772188328332838591917630111621934168250542105416822605376269717082673078820617279401163,
826310506822290205064188178213149159510640222589609259652882078022547937403817214910681508294377070745380596693028828588577263173155859328255115733005548321607382359486995939357538531794140938946533549227507209732744688451838326074988348857950953419716959132561622942987512881279895172760252151216236785075493636479734817032988016751875365574078512390297683769976344810085276896479841795654164608327117441,
5079407915460719891864062039078676848420830460818064839390979658502538005773926044848388042127778582678095139552836355229088103010894407167785007830414253445460540720891961506122246500102763899251877194210170948214886923492433418803176635330226247721619211154524582805019794691494604666104401943187212447892450607418402844123897234048757295179486499912764130930582376034308043165604815951235328482476618961]  #à générer avec le gros ordi

E=[3104397194364553327372889101139121128178906991339821942131441231515968426511387026860919041731698807769876657917543061816313362044093410333119006399990181080671803465090579175634444213793395788135548999601981336944889263852984824316614727513333310087406239045605350167049341404470877369860680632459517349194417513906212826895676205384501595143804635035214425369168030337491220247885483518759057903119514803,
2427345107827418958188820391115719866744313380551643892529646871503421606048984022245329612143709969251010233644469332444152709147300661326639969467351910499867793355502765287755069832957062188763713059079706048104446554074115623011323870259530074225261397063785983420240475650943448578059582982742973499552914800872128396619701729830658682233542467717825157313834548799435844236658308880201543398147819133,
860850389186096825135045477213517908567557574632888089120520868196998187640976823360655724533974093852342521310617497276110693188623115696050177499149830942823201772183068789354527718280706449083503990601773288268611592693526376442180039336121757335038967780754903092464110831734783864692873010707129473374355334428003567336043322287269875908872718693592488308763933757663160045874241632961259704783733023,
7625034545466772162930440368894199667250806225174692134687562284240098032694027515900410061122804964518665609690241068568038262078955031126057945929302669098172099547198271655174648197277027236648668041206804835268961506646766508129912845981862265324223558383776621166662108339672231501795244698041842007317958811736726535058823326081998287700276732765100226899803156144755257354779956042066606947902398331,
5395543489933736526553040867370488081399369071602388617183108100973834733322696390969246053434882227180741047882457751542698553873972794775961981920790890704491099581162324456646094413675637903061992669766887091569158246497368316435410488405311506418751116726589396558567103498022618920290756866889960768686805438223479582122655204268108652420752923963163074840879138393993141230103014789973631920862245057,
2591898223113595043721619042574513717353693059021949644110517239386953549404748136085936882464853754040775854406929341960134140035269899932982393136387336597537791594746707730259585668398930717570732058575490138147160159982959774402320200916422789340748115387466144026694132478531993014208602615968295599848983958464334237846207854823504241183895514228921674248834685413638201159699880111655468407270191969,
3685558584538645620422352295039708446509583850193146507043923631784818097859761409325729363257133280327898064510312989134753992354400982491915441914256641288936654708100726107514884045537520014596108246626866307355009750027007127325242260511821325088542091161194749662823729871353776346065865508140451542583698768847091940397953067137089886589172750329567144472909692601887636895437585933784328965799869,
5179358439507919427978500962540849838679512358617634720309585810152764990083511105501067795917163146294923777910441749102493791635049315883999438764009826761936777347261068362510122643980288918695463880065939705674386387513376277737154656132347756066643234652799032837265069023107620002849489404265924662550302714836753115365396028028418662191336215722287965034372813794810295225361284467016845532230819147,
577791004458006428242130992406002246100532803664660340378318924422177975388199978767521536579645727328114850857623676442683248947096943309448606269313583754552145657449832233586635711879713259318380408205680150751280492763506366385203540909022473207459876766957108085022821413902689119080587443666874301905991267389882486884600881418698247471873166222783617372605490580490967645034373198252158414803153895,
3457591684337502936197026633846921758363174878612537709198300542182609995945546625010126336513874975185320719852430803333351040404871848018439473716926514224100982184680091803514523696544773456070061086941753489394624996892697395591843835159324878322390713267656160592859053577176778467858397803306189466561605375702832861488360153305096507696303475259887759047462457561446464663469498562707651008420815987]

D=[9264454739728240565340987148032743008867697600105370442433882343798537939258693688079604457156225955479680800780825484502848933582972956560695053298019692798887106029179323176332569438138945915557079602287738854314217098502452962440990168743550651479476229422579084377521160160689278517911248645568691954445831052753042633038478510181653189467944210534602505740785383964202385490123827591012464971921554907,
644004429839924141645762438721126434218249691909526201510144174569418593960183019422691084925726628733862836816692411931247871492022728357667412161395728210551214210184113578085832026066670928186513969290877211585372072197434494080634020843340212371954013873329653794578391854815520692049520197344818264005311299991341527797466587271803717037817925713269061469565300631637069484343710900408638835100891797,
2340341035550131611049644112156548844670600536541740019282946654543196306845548513612468686944176479466787378745420867612673457583858952979519884093623372592170706907321246826527965048084240148576155997791190427386633614868514751516661183074040678855472518858390016073239219393314982910366213106633630831781325825089639773173068576551394453884939929112732676234688074856292486290779609765242979677588463775,
1122148607845311437284029331520118495655309186858719720464636677674120138931000500436776942347816676692119573626678476246890877290040995301751792137419869114322461550213980776825946434230264285307876208799948479468575615700710659373938856451646169409104636966758977778684808704459436002941970091056168454099722093285439612889353328044603721654128913386506699539311820366367224921898512962273633095232646947,
2928504725309516216548441940178810522187316020557834384289392821735378879090813024511826511030578327091247057263382646021910587751439411776246177582535968628232052440718001447826775655197520663986132113799350204162730781357947663253444886373855665874764620245809441692345056355280891842430071046653214398396902736385402130294829417100774835830281252018202857353180701991681803833201944255850807019199272561,
3562102487992216429935043075118778661573389548640867310560521685786742770659685233059978878565016538098772326606137372900635829735742137906042936791084098809963113677590168459007282865137685874682224804433815963667388889457639579925302605664649856803835801159891721475215030342211196148516528974855264251654841810989110162166419847662676174926438295533529387248147477460037095403285344222617877007930314805,
15741140230145430521887559988123310831029940340454833701733250705512037708158643423442772477941345323692979245081523389111041056794907082855023685564813179569667769539804968808563761159996409806253332435550629279519302994569227683752689478197202908533995944467934075609014442626788672656159747393568766983816142655374187626176180215183475126730935107910216474315925824430518412861480114581460574715040429,
6154864102664116117103522333598285095112215826713336979384504866715980280931576799641573896694336709836687886245891683527968180174111371089949551364162133802054845872249890811973909765681745794525381619306337588325149221431392633137657104039153614496761553222030922012759955868938521071818487369534450783711387974779070588950815043959207473512011659197694083884767070087400548244490553447450312924344504035,
391295998480791567497024242436231587356078059623019197821594270988508743877019104111326741546470742370317263836592392168406171837488345241056360597085830123562390273231745184325161507195887072677963427279007848979749326885281972899248812230891565315101422542136599012479906849057530952349008272158790572310488776589014446912881324468954020677374072168058165614688671554976020917214114781263028538645251479,
959848483236043571756842017960692474893316929256391068226522717074429872415351738897824156521064899769757212731147513087233838928348283518899627948119639638124867343840110823858284731345704101799751368353325107110145664989744557292918211356350938607238772916578986379707882274043794817534864397007025978566378382995102378080460636822724217138488393804861776466400021777063982874823860055043159763035671915]



test_RSA(10,500,10)
for i in range(10):
    print()
test_RSA(500,10000,83)
