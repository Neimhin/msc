import numpy as np

def convolve(input: np.ndarray, kernel: np.ndarray):
    ishape = input.shape
    kshape = kernel.shape
    assert len(ishape) == 2
    assert len(kshape) == 2
    assert ishape[0] == ishape[1]
    assert kshape[0] == kshape[1]

    oshape = (ishape[0] - kshape[0] + 1, ishape[1] - kshape[1] + 1)
    output = np.zeros(oshape)
    for i in range(oshape[0]):
        for j in range(oshape[1]):
            input_slice = input[i:i+kernel.shape[0],j:j+kernel.shape[1]]
            print(input_slice)
            mul = np.multiply(input_slice, kernel)
            print(mul)
            output[i,j] = mul.sum()
    return output

def test1():
    input = np.zeros((4,4))
    kernel = np.zeros((3,3))
    output = convolve(input,kernel)
    assert(output.shape == (2,2))
    print("passed")

def test2():
    input = np.ones((4,4))
    kernel = input
    output = convolve(input,kernel)
    assert output[0][0] == 16
    print("passed")

def test3():
    input = np.array([[3,3,3],[2,2,2],[1,1,1]])
    kernel = np.identity(2)
    output = convolve(input,kernel)
    assert np.array_equal(output,np.array([[5,5],[3,3]]))
    print("passed")


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2 and sys.argv[1] == "--test":
        test1()
        test2()
        test3()