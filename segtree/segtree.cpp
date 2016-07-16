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

    void render(int i = 1, int covered = false)
    {
        d[i].covered = d[i].covered || covered;
        if (d[i].left + 1 == d[i].right) {
            return;
        }
        render(i * 2, d[i].covered);
        render(i * 2 + 1, d[i].covered);
    }

    void dump_node(int *result, int i = 1)
    {
        if (d[i].covered) {
            for (int j = d[i].left; j < d[i].right; j++) {
                result[++result[0]] = j;
            }
            return;
        }
        if (d[i].left + 1 == d[i].right) {
            return;
        }
        dump_node(result, i * 2);
        dump_node(result, i * 2 + 1);
    }

    int *get_all_covered()
    {
        int *result = new int[length + 1];
        result[0] = 0;
        dump_node(result);
        return result;
    }

    void free_result(int *result)
    {
        delete[] result;
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

    struct st_result
    {
        int i;
        int *result;
        st_result(int *result)
        {
            this->i = 1;
            this->result = result;
        }

        int next()
        {
            if (this->i <= this->result[0]) {
                return this->result[this->i++];
            }
            delete[] this->result;
            return -1;
        }
    };

    DLLEXPORT st_result *st_get_all_covered(void *st)
    {
        SegTree *pst = (SegTree *)st;
        int *result = pst->get_all_covered();
        return new st_result(result);
    }

    DLLEXPORT int st_next_result(st_result *result)
    {
        return result->next();
    }

    DLLEXPORT void st_free(void *st)
    {
        SegTree *pst = (SegTree *)st;
        delete pst;
    }
}

//*
int main()
{
    SegTree *x = new SegTree(7);
    //x->add(0, 3);
    x->add(4, 7);
    x->dump();
    printf("count: %d\n", x->count());
    //x->add(0, 4);
    //x->dump();

    int *result = x->get_all_covered();
    for (int i = 1; i <= result[0]; i++) {
        printf("result[%d] = %d\n", i, result[i]);
    }
    x->free_result(result);

    int v;

    st_result *r = st_get_all_covered(x);
    while ((v = st_next_result(r)) >= 0) {
        printf("result.has %d\n", v);
    }
    return 0;
}
// */
