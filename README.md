## Python with Rust

python中如何使用rust编写的库？

### maturin

maturin是一个工具，可以帮助我们将Rust代码编译成Python模块，并且可以轻松地发布到PyPI上。以下是使用maturin的步骤：

### 创建一个新的Rust库

会在src目录下创建rust库的模板代码：

```bash
maturin init --lib
```

## Python with Rust

python中如何使用rust编写的库？

### maturin

maturin是一个工具，可以帮助我们将Rust代码编译成Python模块，并且可以轻松地发布到PyPI上。以下是使用maturin的步骤：

1. 安装maturin：

```bash
uv init
uv add maturin
```

### 创建一个新的Rust库

会在src目录下创建rust库的模板代码：

```bash
maturin init --lib
```

例子：

```rust
use pyo3::prelude::*;
use pyo3::types::PyDict;

// 定义在 mod Module 外面
#[pyfunction]
fn hello_rust() -> PyResult<String> {
    println!("Hello from Rust!");
    Ok("Hello from Rust!".to_string())
}


// 这里定义了两个Python函数，分别是sum_as_string和hello。
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    // 将a和b相加，并将结果转换为字符串返回
    Ok((a + b).to_string())
}

// 这个函数接受两个参数，一个是i32类型的a，另一个是usize类型的b。函数返回一个i32类型的结果，即a和b的和。
#[pyfunction]
fn hello(a: i32, b: usize) -> PyResult<i32> {
    // 将a和b相加，并将结果返回
    Ok(a + b as i32)
}

#[pyfunction]
fn fib(n: usize) -> PyResult<i64> {
    if n == 0 {
        Ok(0)
    } else if n == 1 {
        Ok(1)
    } else {
        let mut a = 0;
        let mut b = 1;
        for _ in 2..=n {
            let temp = a + b;
            a = b;
            b = temp;
        }
        Ok(b)
    }
}


// 这个函数接受一个整数列表nums，并返回一个字典，其中每个键是输入列表中的整数，值是对应的斐波那契数。函数使用了前面定义的fib函数来计算斐波那契数。
#[pyfunction]
fn fib_map(py: Python<'_>, nums: Vec<i64>) -> PyResult<Bound<'_, PyDict>> {
    let results = PyDict::new(py);
    // 遍历输入的整数列表nums，对于每个整数num，调用fib函数计算对应的斐波那契数，并将结果存储在字典results中，其中键是num，值是fib(num)的结果。
    for num in nums {
        results.set_item(num, fib(num as usize)?)?;
    }
    // 最后，函数返回这个字典results。
    Ok(results)
}

/// A Python module implemented in Rust.
#[pymodule]
fn Module(m: &Bound<'_, PyModule>) -> PyResult<()> {



    // 将外面定义的函数注册进来
    m.add_function(wrap_pyfunction!(hello, m)?)?;
    m.add_function(wrap_pyfunction!(hello_rust, m)?)?;
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(fib, m)?)?;
    m.add_function(wrap_pyfunction!(fib_map, m)?)?;


    Ok(())
}

```

新式 #[pymodule]（当前代码）

- #[pyfunction] 自动暴露，不需要 m.add_function
- 但 m 不在作用域内，无法引用外部函数

老式 fn Module(m: &Bound<'_, PyModule>)（上面的写法）

- m 作为参数传入，add_function 可用
- 外部函数 hello_rust 可以 wrap_pyfunction!(hello_rust, m)? 注册进来
- 内部函数如果不手动 add_function 就不会被暴露（编译警告 "function is never used"）

所以：外面定义的函数能被加进来，但代价是里面定义的也得手动加。 两种风格二选一，不能混用。

### 构建和安装

```bash
maturin develop
```

### 发布到PyPI

```bash
maturin publish
```

### 代码里使用

```python
import Module

print(Module.hello_rust())
print(Module.sum_as_string(1, 2))
print(Module.hello(1, 2))


def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


import time

t1 = time.time()

print(fib(40))
t2 = time.time()
print("Python fib(40) took %s seconds" % (t2 - t1))

print(Module.fib(40))
t3 = time.time()
print("Rust fib(40) took %s seconds" % (t3 - t2))

print(Module.fib_map([1,2,3,4,5,6,7,8,9,10]))
```
