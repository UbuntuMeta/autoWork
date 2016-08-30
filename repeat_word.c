#include<stdio.h>

void main() 
{
    char str[80], *p, *q;
    int isSame = 1;
    scanf("%s", &str);
    p = q = str;
    while(*q)
    {
        q++;
    }
    q--;
    while(p < q)
    {
        if (*p != *q)
        {
            isSame = 0;
            break;
        } else {
            p++;
            q--;
        }
    }

    if (isSame) 
    {
        printf("The string of %s is 回文", str);
    }
    else 
    {
        printf("The string of %s is not 回文", str);
    }
}