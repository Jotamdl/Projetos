#include <stdio.h>
#include <stdlib.h>

struct elemento {
    int num;
    struct elemento *prox;
};
typedef struct elemento Elem;
typedef struct elemento *Lista;

Lista* cria_lista()
{
    Lista *li = (Lista *) malloc(sizeof(Lista));
    *li == NULL;

    return li;
}

int adiciona_elemento(Lista *li, int num)
{
    Elem *no = (Elem *) malloc(sizeof(Elem));
    no->num = num;
    no->prox = NULL;
    
    if (*li == NULL)
    {
        *li = no;
        return 0;
    }
    else
    {
        Elem *aux;
        aux = *li;
        while (aux->prox != NULL)
        {
            aux = aux->prox;
        }
        aux->prox = no;
        return 1;
    }
}

int imprime_itens(Lista *li)
{
    Elem *no = *li;

    while (no != NULL)
    {
        printf("%i ", no->num);
        no = no->prox;
    }
    
}

int main() {
    int A, num, i;

    scanf(" %i", &A);


    Lista *li = cria_lista();

    for (i = 0; i < A; i++)
    {
        scanf(" %i", &num);
        
        adiciona_elemento(li, num);
    }
    
    imprime_itens(li);

    return 0;
}