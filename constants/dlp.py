class DLP_constant:
    def __init__(self, p, q, g, z):
        self.p = p
        self.q = q
        self.g = g
        self.z = z


DLP1024 = DLP_constant(
    p=162155780009993922795212647433960286862704189724389596481093261351292148974073735890519084833831313811262390186468511403269621237103103603695268377255416232083535519897722869772821855517607819731147985323839187982086294829198199728524532697377579141473316365298044665453864810026449411610009818753455641468687,
    q=81077890004996961397606323716980143431352094862194798240546630675646074487036867945259542416915656905631195093234255701634810618551551801847634188627708116041767759948861434886410927758803909865573992661919593991043147414599099864262266348688789570736658182649022332726932405013224705805004909376727820734343,
    g=2,
    z=3
)

DLP2048 = DLP_constant(
    p=18335162836118824998024697275182543802963909807154628975238940777386567884819057198622936701651040745321181914765070523701581791289754838644611646100200941607013502375749175027906045455357893163288227822256675326677769985754504779799270724633229288909953795592810220973720949328449641755339938575695788543522814816748326980326301774358695839767120647009668073822705156952455131543205560608375621847756476300309105966425013284996224020322906945803070410045651065231217621698202267296253230484693885277040770932410324452348271816714171018883083732947729457397010696457125998963033889065803748232997247797734615012233823,
    q=9167581418059412499012348637591271901481954903577314487619470388693283942409528599311468350825520372660590957382535261850790895644877419322305823050100470803506751187874587513953022727678946581644113911128337663338884992877252389899635362316614644454976897796405110486860474664224820877669969287847894271761407408374163490163150887179347919883560323504834036911352578476227565771602780304187810923878238150154552983212506642498112010161453472901535205022825532615608810849101133648126615242346942638520385466205162226174135908357085509441541866473864728698505348228562999481516944532901874116498623898867307506116911,
    g=2,
    z=3
)

DLP3072 = DLP_constant(
    p=5668307579076355587030889847468355311360253132892825768896521107557284950200215515422484513887018928469253870395304302145588801293593826593071667549240950032400856959098945517068858726286264006363890107832960452555347792293042246739545951573284238765813691789999965574599139148490803909166058607406223904327870827386696778486173674734040349564093966364595328558212062552158902285221044373684861243650778772225921543331899174846706882994649472611395549716439598257060470810173900791543089352621656906313779002378333891317676090086041769723698726801180270335404008502747283748359228054026141802300524569904319809036247676299241601391935339000996631928332124429886581391218068790059429024632025662216441319626126962540838198943578501156016523314051874064476106534883261455677119399482718956308657183603796619484986675583382869147661483806562847724971264423392958756387737127067803899658572652905773880408923574557684183489835263,
    q=2834153789538177793515444923734177655680126566446412884448260553778642475100107757711242256943509464234626935197652151072794400646796913296535833774620475016200428479549472758534429363143132003181945053916480226277673896146521123369772975786642119382906845894999982787299569574245401954583029303703111952163935413693348389243086837367020174782046983182297664279106031276079451142610522186842430621825389386112960771665949587423353441497324736305697774858219799128530235405086950395771544676310828453156889501189166945658838045043020884861849363400590135167702004251373641874179614027013070901150262284952159904518123838149620800695967669500498315964166062214943290695609034395029714512316012831108220659813063481270419099471789250578008261657025937032238053267441630727838559699741359478154328591801898309742493337791691434573830741903281423862485632211696479378193868563533901949829286326452886940204461787278842091744917631,
    g=2,
    z=3
)

DLP = DLP3072