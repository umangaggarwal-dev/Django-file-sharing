#include<iostream>
using namespace std;

void quick_sort(int *arr,int low, int high){
    int *right, *left, *loc;
    int len = high-low +1;
    if(len >1){
        left = &arr[low];
        right = &arr[high];
        loc = left;
        while(right!=left){
            if(loc ==left){
                if(*right<*left){
                    int temp;
                    temp = *right;
                    *right = *left;
                    *left = temp;
                    loc = right;
                    left++;
                }
                else{
                    right--;
                }
                continue;
            }
            else if(loc==right){
                if(*left>*right){
                    int temp;
                    temp = *right;
                    *right = *left;
                    *left = temp;
                    loc = left;
                    right++;
                }
                else{
                    left++;
                }
                continue;
            }
        }
        if(left == right){
            cout << "Splitting ";
            for(int i=low; i<high; i++)
                cout << arr[i];
            cout << endl;
            int *ptr;
            ptr = &arr[0];
            int left_len=0, right_len=0, pos;
            while(ptr!=loc){
                ptr++;
                left_len++;
            }
            pos = left_len;
            ptr= &arr[len-1];
            while(ptr!=loc)
            {
                right_len++;
                ptr--;
            }
            quick_sort(&arr[0], low, pos-1);
            quick_sort(&arr[0], pos+1, high);
            cout << "Merging ";
            for(int i=low; i<high; i++)
                cout << arr[i];
            cout << endl;
        }
    }
}



int main(){
    int n;
    cin >> n;
    int a[n];
    int low =0, high=n-1;
    for(int i=0; i<n; i++)
        cin >> a[n];
    quick_sort(&a[0], low, high);
    for(int i=0; i<n; i++)
        cout << a[i]<< ' ';
    cout << endl;
    return 0;
}