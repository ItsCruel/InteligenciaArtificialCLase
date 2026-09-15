#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define epoca 100000
#define K 0.3f

// Funcion sigmoide
float sigmoide(float);

// Pesos de las 2 neuronas ocultas
float PesosH1[2];
float PesosH2[2];

// Pesos de la neurona de salida
float PesosS[2];

// Bias
float biasH1;
float biasH2;
float biasS;

// Inicializar pesos
void pesos_initNt();

// Entrenamiento
float EntNt(float x0, float x1, float target);

// Probar red
float InitNt(float x0, float x1);


float sigmoide(float s)
{
    return 1.0f / (1.0f + expf(-s));
}


void pesos_initNt(void)
{
    PesosH1[0] = (float)rand() / RAND_MAX;
    PesosH1[1] = (float)rand() / RAND_MAX;

    PesosH2[0] = (float)rand() / RAND_MAX;
    PesosH2[1] = (float)rand() / RAND_MAX;

    PesosS[0] = (float)rand() / RAND_MAX;
    PesosS[1] = (float)rand() / RAND_MAX;

    biasH1 = (float)rand() / RAND_MAX;
    biasH2 = (float)rand() / RAND_MAX;
    biasS  = (float)rand() / RAND_MAX;
}


float EntNt(float x0, float x1, float target)
{
    float netH1;
    float netH2;

    float outH1;
    float outH2;

    float netS;
    float outS;

    float error;

    float deltaS;
    float deltaH1;
    float deltaH2;


    // -------------------------
    // CAPA OCULTA
    // -------------------------

    netH1 = PesosH1[0] * x0 +
            PesosH1[1] * x1 +
            biasH1;

    outH1 = sigmoide(netH1);


    netH2 = PesosH2[0] * x0 +
            PesosH2[1] * x1 +
            biasH2;

    outH2 = sigmoide(netH2);


    // -------------------------
    // CAPA DE SALIDA


    netS = PesosS[0] * outH1 +
           PesosS[1] * outH2 +
           biasS;

    outS = sigmoide(netS);


    // -------------------------
    // ERROR
    

    error = target - outS;


    // Delta de salida
    deltaS = error * outS * (1.0f - outS);


    // Delta de neuronas ocultas
    deltaH1 =
        outH1 *
        (1.0f - outH1) *
        PesosS[0] *
        deltaS;


    deltaH2 =
        outH2 *
        (1.0f - outH2) *
        PesosS[1] *
        deltaS;


    
    // ACTUALIZAR PESOS SALIDA
    

    PesosS[0] += K * deltaS * outH1;
    PesosS[1] += K * deltaS * outH2;

    biasS += K * deltaS;


   
    // ACTUALIZAR PESOS OCULTOS

    PesosH1[0] += K * deltaH1 * x0;
    PesosH1[1] += K * deltaH1 * x1;

    biasH1 += K * deltaH1;

    PesosH2[0] += K * deltaH2 * x0;
    PesosH2[1] += K * deltaH2 * x1;

    biasH2 += K * deltaH2;


    return outS;
}


float InitNt(float x0, float x1)
{
    float outH1;
    float outH2;
    float outS;


    outH1 = sigmoide(
        PesosH1[0] * x0 +
        PesosH1[1] * x1 +
        biasH1
    );


    outH2 = sigmoide(
        PesosH2[0] * x0 +
        PesosH2[1] * x1 +
        biasH2
    );


    outS = sigmoide(
        PesosS[0] * outH1 +
        PesosS[1] * outH2 +
        biasS
    );


    return outS;
}


int main()
{
    int i = 0;

    pesos_initNt();


    while(i < epoca)
    {
        // XOR

        EntNt(0,0,0);
        EntNt(0,1,1);
        EntNt(1,0,1);
        EntNt(1,1,0);

        i++;
    }


    printf("\nResultados XOR\n");

    printf("0,0 = %f\n", InitNt(0,0));
    printf("0,1 = %f\n", InitNt(0,1));
    printf("1,0 = %f\n", InitNt(1,0));
    printf("1,1 = %f\n", InitNt(1,1));


    return 0;
}