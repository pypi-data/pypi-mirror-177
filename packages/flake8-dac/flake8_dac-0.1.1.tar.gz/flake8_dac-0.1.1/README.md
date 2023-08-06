# flake8-dac
Tool for formatting flake8's results in more readable way, in case there's a lot of them.
The "dac" part in tool's name stands for "divide and conquer".

### flake8 output with flake8-dac formatting example

- Grouped by the type of cause (with number of occurrences).
- Sorted by the number of occurrences (descending).
- Information about number of problems.
- Rich text and formatting.
- Link to flake8rules.com (where you can find more details about the problem).

![after](https://user-images.githubusercontent.com/50829834/201550776-119d4d52-7244-4672-9b4e-56d58b7e13aa.png)

### flake8 output example

![before](https://user-images.githubusercontent.com/50829834/201550788-35ccaf54-343d-4b3e-812c-498fd1f82dd4.png)


## Installation

```
pip install flake8-dac
```

## Usage

```
flake8 [args] | flake8-dac
```

## Why?

I wrote it for myself when I had to implement flake8 into an existing project that had many problems. I find it helpful when I have problems grouped by the same type of cause. I can easily determine which problems I can ignore, and then eliminate the rest. Maybe someone will find it useful too.
