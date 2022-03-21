Search.setIndex({docnames:["generated/qcp","generated/qcp.matrices","generated/qcp.ui","index","modules","qcp","qcp.algorithms","qcp.cli","qcp.gui","qcp.gui.components","qcp.gui.components.grovers","qcp.gui.components.phase_estimation","qcp.gui.components.sudoku","qcp.matrices","qcp.ui","qcp.ui.components","qcp.ui.widgets"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":4,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,"sphinx.ext.viewcode":1,sphinx:56},filenames:["generated/qcp.rst","generated/qcp.matrices.rst","generated/qcp.ui.rst","index.rst","modules.rst","qcp.rst","qcp.algorithms.rst","qcp.cli.rst","qcp.gui.rst","qcp.gui.components.rst","qcp.gui.components.grovers.rst","qcp.gui.components.phase_estimation.rst","qcp.gui.components.sudoku.rst","qcp.matrices.rst","qcp.ui.rst","qcp.ui.components.rst","qcp.ui.widgets.rst"],objects:{"":[[5,0,0,"-","qcp"]],"qcp.algorithms":[[6,0,0,"-","abstract_algorithm"],[6,0,0,"-","grovers_algorithm"],[6,0,0,"-","phase_estimation"],[6,0,0,"-","sudoku"]],"qcp.algorithms.abstract_algorithm":[[6,1,1,"","GeneralAlgorithm"]],"qcp.algorithms.abstract_algorithm.GeneralAlgorithm":[[6,2,1,"","__init__"],[6,3,1,"","_abc_impl"],[6,2,1,"","construct_circuit"],[6,2,1,"","initial_state"],[6,2,1,"","measure"],[6,2,1,"","run"]],"qcp.algorithms.grovers_algorithm":[[6,1,1,"","Grovers"],[6,4,1,"","pull_set_bits"]],"qcp.algorithms.grovers_algorithm.Grovers":[[6,2,1,"","__init__"],[6,3,1,"","_abc_impl"],[6,2,1,"","construct_circuit"],[6,2,1,"","diffusion"],[6,2,1,"","measure"],[6,2,1,"","single_target_oracle"]],"qcp.algorithms.phase_estimation":[[6,1,1,"","PhaseEstimation"],[6,4,1,"","inverse_qft_gate"],[6,4,1,"","inverse_qft_rotation_gate"],[6,4,1,"","is_unitary"],[6,4,1,"","optimum_qubit_size"],[6,4,1,"","qft_gate"],[6,4,1,"","qft_rotation_gate"]],"qcp.algorithms.phase_estimation.PhaseEstimation":[[6,2,1,"","__init__"],[6,3,1,"","_abc_impl"],[6,2,1,"","construct_circuit"],[6,2,1,"","first_layer"],[6,2,1,"","initial_state"],[6,2,1,"","measure"],[6,2,1,"","second_layer"],[6,2,1,"","third_layer"]],"qcp.algorithms.sudoku":[[6,1,1,"","Sudoku"]],"qcp.algorithms.sudoku.Sudoku":[[6,2,1,"","__init__"],[6,3,1,"","_abc_impl"],[6,2,1,"","construct_circuit"],[6,2,1,"","diffusion"],[6,2,1,"","measure"],[6,2,1,"","measure_solution"],[6,2,1,"","oracle"],[6,2,1,"","sudoku_conditions"]],"qcp.cli":[[7,0,0,"-","constants"],[7,0,0,"-","interpret"],[7,0,0,"-","options"],[7,0,0,"-","parser"],[7,0,0,"-","progress_bar"],[7,0,0,"-","usage"]],"qcp.cli.constants":[[7,5,1,"","ALGORITHM_LONG"],[7,5,1,"","ALGORITHM_SHORT"],[7,5,1,"","DEFAULT_ALGORITHM"],[7,5,1,"","DEFAULT_PHASE"],[7,5,1,"","DEFAULT_TARGET"],[7,5,1,"","DEFAULT_UNITARY"],[7,5,1,"","FLAG_MAPPING"],[7,5,1,"","HELP_LONG"],[7,5,1,"","HELP_SHORT"],[7,5,1,"","PHASE_LONG"],[7,5,1,"","PHASE_SHORT"],[7,5,1,"","TARGET_LONG"],[7,5,1,"","TARGET_SHORT"],[7,5,1,"","UNITARY_LONG"],[7,5,1,"","UNITARY_SHORT"]],"qcp.cli.interpret":[[7,4,1,"","_determine_qbits"],[7,4,1,"","determine_grover"],[7,4,1,"","determine_phase_estimation"],[7,4,1,"","determine_sudoku"],[7,4,1,"","interpret_arguments"]],"qcp.cli.options":[[7,1,1,"","AlgorithmOption"],[7,1,1,"","UnitaryMatrices"]],"qcp.cli.options.AlgorithmOption":[[7,3,1,"","Grovers"],[7,3,1,"","PhaseEstimation"],[7,3,1,"","Sudoku"],[7,2,1,"","get_constructor"],[7,2,1,"","get_name"],[7,2,1,"","list"]],"qcp.cli.options.UnitaryMatrices":[[7,3,1,"","HADAMARD"],[7,3,1,"","PHASE_SHIFT"],[7,2,1,"","get"],[7,2,1,"","list"]],"qcp.cli.parser":[[7,4,1,"","parse_input"],[7,4,1,"","read_cli"]],"qcp.cli.progress_bar":[[7,5,1,"","_ticks"],[7,4,1,"","ticker"]],"qcp.cli.usage":[[7,5,1,"","USAGE_STR"],[7,4,1,"","usage"]],"qcp.constants":[[5,5,1,"","IDENTITY"],[5,5,1,"","ONE_VECTOR"],[5,5,1,"","PAULI_X"],[5,5,1,"","PAULI_Z"],[5,5,1,"","TWO_HADAMARD"],[5,5,1,"","ZERO_VECTOR"]],"qcp.gates":[[5,1,1,"","Gate"],[5,4,1,"","_generic_control"],[5,4,1,"","control_phase"],[5,4,1,"","control_u"],[5,4,1,"","control_x"],[5,4,1,"","control_z"],[5,4,1,"","multi_gate"],[5,4,1,"","phase_shift"],[5,4,1,"","swap"]],"qcp.gates.Gate":[[5,3,1,"","H"],[5,3,1,"","I"],[5,3,1,"","P"],[5,3,1,"","X"],[5,3,1,"","Z"]],"qcp.gui":[[8,0,0,"-","constants"]],"qcp.gui.constants":[[8,5,1,"","THREAD_PAUSE"],[8,5,1,"","UI_FILENAME"]],"qcp.main":[[5,4,1,"","compute"],[5,4,1,"","main"],[5,4,1,"","threaded_progress_bar"]],"qcp.matrices":[[13,3,1,"","DefaultMatrix"],[13,0,0,"-","dense_matrix"],[13,0,0,"-","matrix"],[13,0,0,"-","sparse_matrix"],[13,0,0,"-","types"]],"qcp.matrices.dense_matrix":[[13,1,1,"","DenseMatrix"]],"qcp.matrices.dense_matrix.DenseMatrix":[[13,2,1,"","__add__"],[13,2,1,"","__getitem__"],[13,2,1,"","__init__"],[13,2,1,"","__len__"],[13,2,1,"","__mul__"],[13,2,1,"","__setitem__"],[13,2,1,"","__str__"],[13,2,1,"","__sub__"],[13,3,1,"","_abc_impl"],[13,2,1,"","_dot"],[13,2,1,"","columns"],[13,2,1,"","conjugate"],[13,2,1,"","get_state"],[13,2,1,"","identity"],[13,6,1,"","num_columns"],[13,6,1,"","num_rows"],[13,2,1,"","rows"],[13,2,1,"","trace"],[13,2,1,"","transpose"],[13,2,1,"","zeros"]],"qcp.matrices.matrix":[[13,1,1,"","Matrix"]],"qcp.matrices.matrix.Matrix":[[13,2,1,"","__add__"],[13,2,1,"","__getitem__"],[13,2,1,"","__init__"],[13,2,1,"","__len__"],[13,2,1,"","__mul__"],[13,2,1,"","__rmul__"],[13,2,1,"","__setitem__"],[13,2,1,"","__str__"],[13,2,1,"","__sub__"],[13,3,1,"","_abc_impl"],[13,2,1,"","_optional_newline"],[13,2,1,"","adjoint"],[13,2,1,"","columns"],[13,2,1,"","conjugate"],[13,2,1,"","get_state"],[13,6,1,"","num_columns"],[13,6,1,"","num_rows"],[13,6,1,"","square"],[13,2,1,"","trace"],[13,2,1,"","transpose"]],"qcp.matrices.sparse_matrix":[[13,1,1,"","SparseMatrix"],[13,1,1,"","SparseVector"],[13,4,1,"","_list_to_dict"]],"qcp.matrices.sparse_matrix.SparseMatrix":[[13,2,1,"","__add__"],[13,2,1,"","__getitem__"],[13,2,1,"","__init__"],[13,2,1,"","__len__"],[13,2,1,"","__mul__"],[13,2,1,"","__setitem__"],[13,2,1,"","__str__"],[13,2,1,"","__sub__"],[13,3,1,"","_abc_impl"],[13,2,1,"","_as_list"],[13,2,1,"","_dot"],[13,2,1,"","_dot_sparse"],[13,2,1,"","_get_row"],[13,2,1,"","columns"],[13,2,1,"","conjugate"],[13,2,1,"","get_state"],[13,2,1,"","identity"],[13,6,1,"","num_columns"],[13,6,1,"","num_rows"],[13,2,1,"","rows"],[13,2,1,"","trace"],[13,2,1,"","transpose"],[13,2,1,"","zeros"]],"qcp.matrices.sparse_matrix.SparseVector":[[13,2,1,"","__getitem__"],[13,2,1,"","__init__"],[13,2,1,"","__len__"],[13,2,1,"","__setitem__"]],"qcp.matrices.types":[[13,5,1,"","MATRIX"],[13,5,1,"","SCALARS"],[13,5,1,"","SCALARS_T"],[13,5,1,"","SPARSE"],[13,5,1,"","VECTOR"]],"qcp.register":[[5,4,1,"","_magnitude"],[5,4,1,"","measure"]],"qcp.tensor_product":[[5,4,1,"","_tensor_product_sparse"],[5,4,1,"","tensor_product"]],qcp:[[6,0,0,"-","algorithms"],[7,0,0,"-","cli"],[5,0,0,"-","constants"],[5,0,0,"-","gates"],[8,0,0,"-","gui"],[5,0,0,"-","main"],[13,0,0,"-","matrices"],[5,0,0,"-","register"],[5,0,0,"-","tensor_product"]]},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","attribute","Python attribute"],"4":["py","function","Python function"],"5":["py","data","Python data"],"6":["py","property","Python property"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:attribute","4":"py:function","5":"py:data","6":"py:property"},terms:{"0":[3,5,6,7,8],"01":8,"0j":5,"0th":5,"1":[3,5,6,13],"10":7,"125":6,"16":6,"1j":6,"2":[3,5,6,7],"25":[3,7],"2d":13,"2x2":[3,5,6],"3":[6,7],"4":6,"8":7,"9":6,"9th":6,"case":[3,13],"class":[1,5,6,7,13],"default":[3,7,13],"do":[1,3,13],"enum":[5,7],"final":6,"float":[3,5,6,7,13],"function":[5,8,13],"int":[5,6,7,13],"long":7,"new":[3,13],"return":[5,6,7,13],"short":7,"static":13,"true":6,"while":3,A:[3,5,7,13],As:3,At:3,For:[3,6],If:[3,13],In:6,The:[3,5,6,7,8,13],There:3,These:3,To:3,__add__:13,__getitem__:13,__init__:[6,13],__len__:13,__mul__:13,__rmul__:13,__setitem__:13,__str__:13,__sub__:13,_abc:[6,13],_abc_data:[6,13],_abc_impl:[6,13],_as_list:13,_determine_qbit:7,_dot:13,_dot_spars:13,_generic_control:5,_get_row:13,_io:7,_list_to_dict:13,_magnitud:5,_optional_newlin:13,_tensor_product_spars:5,_tick:7,abc:[6,13],abov:3,abstract_algorithm:[4,5],abstract_compon:[5,8,14],accept:[3,7],across:6,act:6,action:3,activ:3,actual:7,add:[7,13],addit:13,adjoint:13,against:13,alg_nam:5,algorithm:[4,5,7],algorithm_long:7,algorithm_short:7,algorithmopt:7,alia:13,all:[1,3,5,6,7,8,13],alloc:13,allow:[3,13],along:13,also:3,amplifi:6,amplitud:[5,6],an:[3,5,6,7,13],angl:5,ani:[3,7,13],anim:7,anoth:13,appear:3,append:13,appli:[5,6,13],appropri:13,ar:[3,6,8,13],arbitrarili:5,arg:[3,5,7],argument:7,argv:7,art:7,ascii:7,associ:6,automat:3,automaticali:3,auxiliari:6,avail:7,awar:3,b:5,background:3,bar:[5,7],base:[0,5,6,7,13],basi:6,been:6,befor:7,begin:3,behaviour:13,being:[3,5,13],besid:3,between:[5,7,13],bin:[3,7],bit:[5,6,7],board:6,bool:[6,13],both:13,bottom:3,bound:[3,13],bring:3,build:7,button_compon:[8,9,14],calcul:[3,5,13],can:[3,5,6,7,13],capabl:3,cd:3,certain:[6,7],chang:[1,3,6,13],charact:13,check:6,choic:[3,5,7],choos:3,chosen:[3,7],circuit:[5,6],classic:3,classmethod:7,cli:[3,4,5],click:3,close:6,cnot:6,code:[3,5,7,8],column:[3,5,6,13],com:3,combin:6,combo_box_compon:[5,8],command:3,compar:3,complet:[3,6],complex:[3,5,13],complic:3,compon:[5,8,14],composit:[5,6],comput:[0,5],cond1:6,cond4:6,condit:[6,13],configur:3,conform:13,conjug:13,consid:13,consider:13,constant:4,construct:[5,6],construct_circuit:6,constructor:[5,7],contain:[1,5,7,13],content:4,context:5,control:[3,5,6,8],control_phas:5,control_u:5,control_x:5,control_z:5,convert:[5,7,13],correspond:[6,7],creat:[5,6,7,13],current:[3,13],current_qubit:6,cval:5,decim:6,default_algorithm:7,default_phas:7,default_target:7,default_unitari:7,defaultmatrix:[1,6,13],defin:[7,8],dens:13,dense_matrix:[4,5],densematrix:13,depend:13,determ:7,determin:[3,5,6,13],determine_grov:7,determine_phase_estim:7,determine_sudoku:7,diagon:13,dict:[7,13],dictionari:[7,13],differ:[3,7],diffus:6,dimenion:13,dimens:13,directli:13,displai:[3,7],distribut:[3,5],dot:13,down:3,download:3,draw:3,drop:3,durat:8,e:[3,6],each:[3,5,6,13],easier:3,effici:6,eigenvalu:6,eigenvector:[3,6,7],either:13,element:[3,13],empti:[5,13],encod:7,enforc:6,entir:6,entri:[3,13],entrypoint:5,environ:3,equival:[3,13],error:[3,6,7],estim:[6,7],event:8,exampl:6,except:3,exit:7,exp:6,expect:13,explicit:3,exponenti:3,extra:3,fault:3,field:3,figur:3,file:[7,8],filenam:8,find:[3,6],first:[3,5,6,7,13],first_lay:6,firstli:7,fix:13,flag:[3,7],flag_map:7,flip:13,follow:[3,6,7],form:8,fourier:6,from:[5,7,13],g:[3,7],gate:[3,4,6,7],gener:5,generalalgorithm:6,get:[3,7,13],get_constructor:7,get_nam:7,get_stat:13,git:3,github:3,give:3,given:[5,7,13],graph:3,graph_compon:[5,8,14],graphic:3,grover:[5,6,7,8,9],grovers_algorithm:[4,5],gui:[4,5],h:[3,5,7,13],ha:3,hadamard:[3,5,6,7],hang:5,have:[1,3,6,13],height:13,help:[3,7],help_long:7,help_short:7,helper:13,here:7,highest:13,horizont:13,hostedtoolcach:7,http:3,i:[5,6,7,13],ident:[3,5,6,13],implement:[1,3,5,6,13],includ:13,increas:6,index:[3,5,13],indic:[7,13],individu:3,infer:13,initi:6,initial_st:6,initialis:[3,8,13],inplac:13,input:[3,6,7],input_compon:[8,9,14],instal:3,intcurrent_qubit:6,integ:3,interact:[3,8],interfac:3,interpret:[4,5],interpret_argu:7,interv:7,invers:6,inverse_qft_g:6,inverse_qft_rotation_g:6,is_unitari:6,issu:3,item:[6,13],iter:[3,13],its:6,kei:13,label:3,later:[1,13],layer:[6,13],layout:[3,8],limit:13,line:[1,13],list:[3,5,6,7,13],live:7,logic:5,longer:3,look:13,m:[3,5],magnitud:5,main:[3,4],main_window:[4,5],make:[3,6],manag:8,manual:3,map:[7,13],mat:5,match:[7,13],math:6,matric:[3,4,5,6,7],matrix:[1,3,4,5,6,7],matter:13,maximis:6,measur:[5,6],measure_solut:6,mechan:5,memori:13,messag:[3,7],met:6,method:13,mirror:13,mode:7,modifi:[1,13],modul:[0,1,3,4],more:[5,7],most:3,move:3,mulitpli:13,multi_g:5,multipl:13,multipli:13,multiprocess:5,must:[3,6,7],mypi:3,n:[5,6,7,13],name:[5,7],ncol:13,need:[3,5,7,13],nest:13,newlin:13,next:3,nflag:7,ngrover:7,nice:3,non:13,none:[3,7],normalis:5,note:3,nphase:7,nqbit:[3,7],nrow:13,nsudoku:7,nthe:7,num_column:13,num_row:13,number:[3,5,6,7,13],o:7,obj:7,object:[5,6,13],observ:[5,6],off:[7,13],onc:3,one:[3,5,6,7,13],one_vector:5,onli:13,oper:[3,7,13],opt:7,optimis:13,optimum_qubit_s:6,option:[4,5,6,13],oracl:[6,7],order:13,other:[6,13],our:[6,13],out:6,output:[3,6],overload:13,overrid:[7,13],overview:3,overwritten:[3,13],p:[3,5,7],packag:4,page:3,pair:13,param:6,paramet:[3,5,6,7,13],parma:7,pars:[5,7],parse_input:7,parser:[4,5],pass:5,pauli:5,pauli_x:5,pauli_z:5,pe:[3,6,7],pep8:3,per:5,perform:6,phase:[5,6,7],phase_esim:6,phase_estim:[4,5,8,9],phase_long:7,phase_shift:[5,7],phase_short:7,phaseestim:[6,7],phi:5,pi:6,pin:3,pip:3,place:13,plot:3,point:3,popul:3,possibl:6,pre:13,precis:6,prefer:[1,13],prefix:7,print:[5,6,7,13],probabl:[3,5,6],problem:[3,6],process:5,product:[5,13],program:3,progress:[3,5,7],progress_bar:[4,5],progress_bar_compon:[5,8],prompt:[3,7],properti:13,provid:[3,7,13],pull_set_bit:6,pure:[1,13],py:[3,6,7],pypi:3,python:[1,3,7,13],q:5,qbibt:3,qbit:[3,5,7],qcp:3,qft:6,qft_gate:6,qft_rotation_g:6,quantum:[0,5,6,7],quantum_computing_project:3,qubit:[5,6],quick:[1,13],quit:3,r2:6,r:[3,6],randomli:6,rate:6,read:[5,7,13],read_cli:7,readi:3,reduc:6,refer:5,referenc:[1,13],reflect:3,refresh:7,regist:[4,6],rel:6,relat:8,relev:6,repeat:6,repres:[5,6],represent:[6,13],requir:[3,5,6,7,13],reset:6,respect:6,result:[3,5,13],right:3,rotat:6,row:13,rtype:6,rule:13,run:[5,6,7],s:[5,6,7,13],said:6,same:[3,13],sampl:3,save:13,scalar:[5,13],scalars_t:13,scale:13,search:7,second:[3,5,7,8,13],second_lay:6,see:[3,6],segu:3,select:6,self:6,separ:[5,13],sequenc:3,set:[3,6,13],shift:[3,5,6,7],shim:13,shortcut:13,show:[3,7],shown:3,signal:8,simpl:3,simul:[0,3,5,6,7],simulator_compon:[8,9,14],single_target_oracl:6,size:[3,5,6,13],sleep:[5,7],so:[1,3,5,13],solut:6,solutions_t:[8,9],solv:[3,6],solver:[3,7],sourc:[3,5,6,7,13],spars:13,sparse_matrix:[4,5],sparsematric:5,sparsematrix:[5,13],sparsevector:13,specif:[5,6],specifi:5,sphinx:7,squar:13,start:[3,8],state:[3,5,6,7,13],stdout:[5,7],still:3,storag:13,store:[6,13],str:[5,6,7,13],string:[7,13],stub:13,submodul:4,subpackag:4,subtract:13,sudoku:[4,5,7,8,9],sudoku_condit:6,suitabl:13,sum:13,swap:5,swirl:7,sy:7,system:[3,6],t:[3,7],take:[3,7],taken:13,target0:5,target1:5,target:[3,5,6,7],target_long:7,target_short:7,target_st:6,tensor:[5,6],tensor_product:4,term:6,termin:7,text:7,textio:7,textiowrapp:7,them:13,thi:[1,3,5,6,7,13],third:7,third_lay:6,thread:8,thread_paus:8,threaded_comput:[5,8],threaded_progress_bar:5,three:3,tick_rat:7,ticker:[5,7],tiernan8r:3,toi:[3,7],took:3,top:3,total:[5,6,13],tox:3,trace:13,transform:6,transpos:13,tupl:[6,7,13],turn:6,twice:6,two:[3,5,7,13],two_hadamard:5,txt:3,type:[1,4,5,6,7],typl:13,u:[3,5,6,7],ui:8,ui_filenam:8,under:13,union:[5,13],unitari:[3,5,6,7],unitary_long:7,unitary_short:7,unitarymatric:7,unless:13,unset:[3,7],until:6,up:[3,13],updat:3,us:[1,3,5,6,7,13],usabl:7,usag:[3,4,5],usage_str:7,user:3,usual:5,utf:7,v0:6,v1:6,v2:6,v3:6,v:[5,13],val:[7,13],valid:6,valu:[5,7,13],vari:[3,5,7],variabl:6,vector:[3,5,6,13],venv:3,verbos:7,verifi:3,virtual:3,virtualenv:3,virtualenviron:3,visual:3,w:[7,13],wai:[3,5],wait:8,want:[1,5,6,13],we:[1,3,5,6,13],weight:6,were:6,when:[3,7,8,13],where:[3,8,13],whether:[6,13],which:[3,5,6,13],whose:6,widg:8,width:13,within:3,without:5,work:3,would:6,x64:7,x:[5,6],xml:8,xor:6,you:3,your:3,z:5,zero:13,zero_vector:5},titles:["qcp","qcp.matrices","qcp.ui","Welcome to Quantum Computing Project\u2019s documentation!","qcp","qcp package","qcp.algorithms package","qcp.cli package","qcp.gui package","qcp.gui.components package","qcp.gui.components.grovers package","qcp.gui.components.phase_estimation package","qcp.gui.components.sudoku package","qcp.matrices package","qcp.ui package","qcp.ui.components package","qcp.ui.widgets package"],titleterms:{abstract_algorithm:6,abstract_compon:[9,15],algorithm:[3,6],applic:3,button:3,button_compon:[10,11,12,15],cli:7,clone:3,combo_box_compon:9,compon:[9,10,11,12,15],comput:3,constant:[5,7,8,9,10,11,12,14],content:[3,5,6,7,8,9,10,11,12,13,14,15,16],dense_matrix:13,document:3,embedded_graph:16,estim:3,gate:5,graph_compon:[9,15],graph_widget:16,grover:[3,10],grovers_algorithm:6,gui:[3,8,9,10,11,12],indic:3,input_compon:[10,11,15],interpret:7,main:[5,8,14],main_window:[8,14],matric:[1,13],matrix:13,modul:[5,6,7,8,9,10,11,12,13,14,15,16],option:[3,7],packag:[5,6,7,8,9,10,11,12,13,14,15,16],parser:7,phase:3,phase_estim:[6,11],progress_bar:7,progress_bar_compon:9,project:3,qcp:[0,1,2,4,5,6,7,8,9,10,11,12,13,14,15,16],quantum:3,regist:5,repositori:3,run:3,s:3,search:3,setup:3,simulator_compon:[10,11,12,15],solutions_t:12,sparse_matrix:13,submodul:[5,6,7,8,9,10,11,12,13,14,15,16],subpackag:[5,8,9,14],sudoku:[3,6,12],tabl:3,tensor_product:5,test:3,threaded_comput:9,type:13,ui:[2,14,15,16],usag:7,welcom:3,widget:16}})