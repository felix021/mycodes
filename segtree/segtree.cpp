#include<iostream>
#include<algorithm>
#include<cstdio>
#include<cstdlib>
#include<cstring>
#include<cmath>
#include<set>
#include<map>
#include<vector>
using namespace std;
#ifdef __DEBUG__
#define dp(fmt, x...) fprintf(stderr, "[%d] " fmt, __LINE__, ##x)
#else
#define dp(fmt, x...)
#endif

int up2(int x)
{
    int t = 1;
    while (x > 0) {
        t <<= 1;
        x >>= 1;
    }
    return t;
}

struct node {
    int left, right;
    bool covered;
    node () {
        left = right = 0;
        covered = false;
    }
};

struct SegTree
{
    int length;
    node *d;

    SegTree(int length)
    {
        this->length = length;
        this->d = new node[up2(length) * 2];
        this->make(1, 0, length);
    }

    ~SegTree()
    {
        delete[] this->d;
    }

    void make(int i, int left, int right, int depth = 0)
    {
        this->d[i].left = left;
        this->d[i].right = right;
        if (left + 1 == right) {
            return;
        }

        int middle = (left + right) / 2;
        this->make(i * 2, left, middle, depth + 1);
        this->make(i * 2 + 1, middle, right, depth + 1);
    }

    bool add(int left, int right)
    {
        if (left < 0 || right > this->length) {
            return false; 
        }
        add_inner(1, left, right);
        return true;
    }

    void add_inner(int i, int left, int right)
    {
        //printf("add(%d, %d, %d) @ [%d, %d)\n", i, left, right, d[i].left, d[i].right);
        if (left == d[i].left && right == d[i].right) {
            d[i].covered = true;
            return;
        }
        int middle = (d[i].left + d[i].right) / 2;
        //printf("  middle = %d\n", middle);
        if (right <= middle) {
            add_inner(i * 2, left, right);
        } else if (left >= middle) {
            add_inner(i * 2 + 1, left, right);
        } else {
            add_inner(i * 2, left, middle);
            add_inner(i * 2 + 1, middle, right);
        }
        d[i].covered = d[i * 2].covered && d[i * 2 + 1].covered;
    }

    void dump(int i = 1, int depth = 0)
    {
        for (int j = 0; j < depth; j++) {
            printf("  ");
        }
        printf("%3d: [%d, %d) => %d\n", i, d[i].left, d[i].right, d[i].covered);
        if (d[i].left + 1 == d[i].right) {
            return;
        }
        dump(i * 2, depth + 1);
        dump(i * 2 + 1, depth + 1);
    }

    int count(int i = 1)
    {
        if (d[i].covered) {
            return d[i].right - d[i].left;
        }
        if (d[i].left + 1 == d[i].right) {
            return 0;
        }
        return count(i * 2) + count(i * 2 + 1);
    }

    void dump_node(int i = 1)
    {
        if (d[i].covered) {
            for (int j = d[i].left; j < d[i].right; j++) {
                printf("%d ", j);
            }
            return;
        }
        if (d[i].left + 1 == d[i].right) {
            return;
        }
        dump_node(i * 2);
        dump_node(i * 2 + 1);
        if (i == 1)
            printf("\n");
    }

    void render(int i = 1, int covered = false)
    {
        d[i].covered = d[i].covered || covered;
        if (d[i].left + 1 == d[i].right) {
            return;
        }
        render(i * 2, d[i].covered);
        render(i * 2 + 1, d[i].covered);
    }

    int next(int i = 0)
    {
        if (d[i].right == length) {
            return -1;
        }

        if (i == 0) {
            for (i = 1; d[i].left + 1 < d[i].right; i *= 2);
            return i;
        }

        int parent = i;
        do {
            parent /= 2;
        } while (d[i].right >= d[parent].right);

        int child = parent * 2 + 1;
        while (d[child].left + 1 != d[child].right) {
            child *= 2;
        }
        return child;
    }

    int position(int i)
    {
        return d[i].left;
    }

    int covered(int i)
    {
        return d[i].covered;
    }
};


#ifdef __WIN32
#define DLLEXPORT __declspec(dllexport)
#else
#define DLLEXPORT
#endif

extern "C" {
    DLLEXPORT void * st_new(int length)
    {
        SegTree *pst = new SegTree(length);
        return (void *) pst;
    }

    DLLEXPORT void st_add(void *st, int left, int right)
    {
        SegTree *pst = (SegTree *)st;
        pst->add(left, right);
    }

    DLLEXPORT int st_count(void *st)
    {
        SegTree *pst = (SegTree *)st;
        return pst->count();
    }

    DLLEXPORT void st_dump(void *st)
    {
        SegTree *pst = (SegTree *)st;
        pst->dump();
    }

    DLLEXPORT int *st_iter(void *st)
    {
        SegTree *pst = (SegTree *)st;
        pst->render();
        return new int(pst->next(0));
    }

    DLLEXPORT int st_next(void *st, int *piterator)
    {
        SegTree *pst = (SegTree *)st;
        while (*piterator > 0) { 
            int iterator = *piterator;
            *piterator = pst->next(*piterator);
            if (pst->covered(iterator)) {
                return pst->position(iterator);
            }
        }
        delete piterator;
        return -1;
    }

    DLLEXPORT void st_free(void *st)
    {
        SegTree *pst = (SegTree *)st;
        delete pst;
    }
}

/*
int main()
{
    SegTree *x = new SegTree(7);
    //x->add(0, 3);
    x->add(4, 7);
    x->dump();
    printf("count: %d\n", x->count());
    x->add(0, 4);
    x->dump();

    int *piter = st_iter(x), v;
    while ((v = st_next(x, piter)) >= 0) {
        printf("%d\n", v);
    }
    return 0;
}
// */
