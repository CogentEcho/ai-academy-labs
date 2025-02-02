# Example Lesson: Understanding Neural Networks

## Lesson: Neural Networks Basics
_Location: curriculum/modules/neural-networks/basics.md_

```markdown
---
title: "Introduction to Neural Networks"
description: "Learn how neural networks process information, similar to how our brains work"
access_options:
  - type: web
    url: /neural-networks/basics
  - type: colab
    url: https://colab.research.google.com/neural-networks-intro
prerequisites:
  required:
    - Basic Python
    - Basic Algebra
  optional:
    - Basic Calculus
estimated_time: "45 minutes"
---

# Understanding Neural Networks

## Real-World Analogy
Imagine you're learning to identify dogs. Your brain processes information like:
- Does it have fur?
- Does it bark?
- How many legs does it have?

Neural networks work similarly, but with numbers!

## Interactive Example

Try our [Neural Network Playground](#demo-1) to see how a simple neural network learns.

## Core Concepts

1. **Neurons**
   - Like tiny decision-makers
   - Each takes multiple inputs
   - Produces a single output

2. **Connections**
   - Carry information between neurons
   - Have "weights" (importance)
   - Can be strengthened or weakened

## Hands-on Activity

[Open in Colab](https://colab.research.google.com/neural-networks-intro)

```python
import numpy as np

# Create a simple neuron
def neuron(inputs, weights):
    return np.dot(inputs, weights) > 0

# Try it!
inputs = [1, 0, 1]
weights = [0.5, -0.1, 0.2]
output = neuron(inputs, weights)
print(f"Neuron output: {output}")
```

## Check Your Understanding

1. What is the main purpose of a neuron in a neural network?
2. How do connections help in processing information?
3. Try modifying the weights in the code above - what happens?

## Next Steps
- [Advanced Neural Networks](../advanced/index.md)
- [Building Your First Model](../first-model/index.md)
```

## Interactive Demo: Neural Network Playground
_Location: demos/neural-networks/playground.html_

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neural Network Playground</title>
</head>
<body>
    <div id="nn-playground" class="container mx-auto px-4 py-8">
        <!-- Demo implementation here -->
    </div>
    
    <script>
        class NeuralNetworkDemo {
            constructor() {
                this.setupNetwork();
                this.bindEvents();
            }

            setupNetwork() {
                // Network setup code
            }

            bindEvents() {
                // Event handling
            }
        }
    </script>
</body>
</html>
```

## Colab Notebook
_Location: notebooks/neural-networks/intro.ipynb_

```python
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Neural Networks Introduction\n",
    "\n",
    "This notebook provides hands-on experience with neural networks."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Setup\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "%matplotlib inline"
   ]
  }
 ]
}
```
