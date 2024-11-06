#include <stdio.h>
#include <stdlib.h>


double **createMat(int m,int n);
double **Matadd(double **a, double **b, int m, int n);//add two matrices
double **Matscale(double **a, int m, int n, double k);
double **Matsec(double **a, double ** b, int m, double k);

/*int main(void)
{
       
    int m = 2; 
    double k = 3.0; 

   
    double **a = (double **)malloc(m * sizeof(double *));
    double **b = (double **)malloc(m * sizeof(double *));
    double **c = (double **)malloc(m*sizeof(double *));
    double **d = (double **)malloc(m*sizeof(double *));
    for (int i = 0; i < m; i++) {
        a[i] = (double *)malloc(1 * sizeof(double));
        b[i] = (double *)malloc(1 * sizeof(double));
        c[i]=(double *)malloc(1*sizeof(double));
        d[i]=(double *)malloc(1*sizeof(double));
    }
    
    
    
    for (int i = 0; i < m; i++) {
        a[i][0] = i + 1; 
        b[i][0] = (i + 1) * 2; 
    }
   
    c= Matadd(Matscale(a,m,1,2),Matscale(b,m,1,-3),m,1);
    d= Matadd(Matscale(a,m,1,1),Matscale(b,m,1,1),m,1);
    //for(int i=0;i<m;i++)
    
	 //   printf("%lf %lf",c[i][0],d[i][0]);
    
    
    double **temp = Matsec(c, d, m, k);

    FILE *file = fopen("output.txt", "w");
    if (file == NULL) {
        printf("Error opening the file!\n");
        return 1;
    }

    
    
    for (int i = 0; i < m; i++) {
	fprintf(file, "%lf ", *a[i]);
        fprintf(file, "%lf \n", temp[i][0]);
    }

    
    fclose(file);
    
    for (int i = 0; i < m; i++) {
        free(a[i]);
        free(b[i]);
        free(temp[i]);
    }
    free(a);
    free(b);
    free(temp);

    return 0;
}*/


	
	
        

double **createMat(int m,int n)
{
 int i;
 double **a;
 
 
a = (double **)malloc(m * sizeof( *a));
    for (i=0; i<m; i++)
         a[i] = (double *)malloc(n * sizeof( *a[i]));

 return a;
}

double **Matsec(double **a, double ** b, int m, double k){
	double **temp=createMat(m,1);
	temp = Matscale(Matadd(a,Matscale(b,m,1,k),m,1),m,1,1/(k+1));
	return temp;
}
double **Matadd(double **a,double **b, int m, int n){
int i, j;
double **c;
c = createMat(m,n);

 for(i=0;i<m;i++)
 {
  for(j=0;j<n;j++)
  {
c[i][j]= a[i][j]+b[i][j];
  }
 }
return c;
}
double **Matscale(double **a, int m, int n, double k){
int i, j;
double **c;
c = createMat(m,n);

 for(i=0;i<m;i++)
 {
  for(j=0;j<n;j++)
  {
c[i][j]= k*a[i][j];
  }
 }
return c;
}

