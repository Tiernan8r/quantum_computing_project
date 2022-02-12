public class Gate:LazyMatrix{
private SquareMatrix sm;
private int smDim;
private int [] qbpos;
public override Vector Apply(Vector v){
Vector w = new Vector(Dimension);
for (int i = 0; i < Dimension; i++){
int r = gather(i);
int i0 = i & ~scatter(r);
for(int c = 0; c<smDim ; c++){
int j = i0 | scatter(c);
w[i] += sm[r,c]*v[j];}
return w; }
private int gather(int i){
int j = 0;
for (int k = 0; k < qbpos.Length;k++) j |= ((i >> qbpos [k]) & 1) << k;
return j;}
private int scatter(int j){
int i = 0;
for (int k = 0; k < qbpos.Length; k++) i |= ((j >> k) & 1) << qbpos [k];
return i;}
}