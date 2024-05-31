## Summary from the course How Diffusion Models Work (deeplearning.ai)


- **Chapter 1:**: Neural Network Architecture: U-Net
- **Chapter 2:** Training a Neural Network (NN) to Predict Noise with DDPM method and UNet architecture**
- **Chapter 3:** Controlling Models Through Embeddings
- **Chapter 4:** Reasons for Slow Sampling Process

___

# Chapter 1: Neural Network Architecture: U-Net

**Introduction:**
- U-Net is one of the most famous and important segmentation architectures.
- It was developed in 2015, specifically to learn from small samples.
- The input and output have the same size.

**U-Net Structure:**
1. **Encoder (Contracting Path):**
   - Receives the input image and extracts important features through multiple convolutional layers.
   - Performs down-sampling, reducing the image resolution by half at each level while increasing the number of channels to capture high-level information.
   
2. **Decoder (Expansive Path):**
   - Performs up-sampling of the features using transposed convolutions.
   - Concatenates the recovered features with the corresponding features from the encoder through skip connections.
   - As a result, produces a segmented mask of the original input image.

**Skip Connections:**
- **Definition:**
  - Direct connections that link corresponding layers of the encoder and decoder.
- **Functioning:**
  - At each down-sampling level in the encoder, the output of the convolutional layers is saved.
  - During the up-sampling process in the decoder, these saved features are concatenated (or added) with the corresponding features from the decoder.
  - They allow the network to use both high-level features (extracted by the encoder) and low-level features (recovered by the skip connections).
- **Benefits:**
  - Preservation of low-level information, such as edges, textures, and fine details.
  - Improved segmentation accuracy by combining information from different resolution levels.

**Down-sampling and Up-sampling Process (with DDPM):**
- **Down-sampling:**
  - Reduces the spatial resolution of the image by half at each level, preserving the main features and patterns.
  - Compresses the information into a smaller space.
- **Up-sampling:**
  - Increases the spatial resolution to recover the original image dimension.
  - Predicts the details that were reduced during down-sampling, using the embedded information.

**Summary:**
- U-Net is effective for image segmentation, allowing the capture and integration of information at multiple scales through its symmetric structure and the use of skip connections.


<img src="/side_projects_diffusion/DL_diffusion_course/imgs/unet_architecture.png" alt="U-Net Architecture" width="600">

<img src="/side_projects_diffusion/DL_diffusion_course/imgs/encoder_decoder_skipconnections.png" alt="Encoder-Decoder with Skip Connections" width="600">

<img src="/side_projects_diffusion/DL_diffusion_course/side_projects_diffusion/imgs/encoder_decoder_skipconnections.png" alt="Encoder-Decoder with Skip Connections" width="600">
___
___
___

# Chapter 2: Training a Neural Network (NN) to Predict Noise with DDPM method and UNet architecture

The objective is to train a neural network to predict noise by teaching it to differentiate between noise and non-noise.

#### Training Steps:
<img src="/side_projects_diffusion/DL_diffusion_course/imgs/training_flow.png" alt="Training flow on code" width="600">


1. **Combining Sprite and Noise:**
   - Add noise to an image (sprite), resulting in a new image that contains the original sprite with noise.
   
2. **Noise Prediction by the Neural Network:**
   - The neural network is tasked with predicting the noise present in the combined image.
   
3. **Comparison and Loss Calculation:**
   - Compare the noise predicted by the neural network with the actual noise added to the image.
   - Based on this comparison, calculate the loss.

4. **Backpropagation:**
   - Use the loss value to perform backpropagation in the neural network.
   - The neural network adjusts its weights and biases based on the calculated loss, gradually improving its ability to predict noise.

5. **Training with Multiple Sprites:**
   - Repeat the process for several images (sprites) with different noises.
   - Train the neural network with multiple losses from different sprites over several epochs.
   - This continuous training process allows the neural network to learn to predict noise more effectively over time.

#### Benefits of the Method:

- **Diversity of Data:**
  - By training with diverse sprites and noises, the neural network becomes more robust and better generalizes its predictions.
  
- **Efficiency in Learning:**
  - Using multiple losses over different epochs improves the neural network's learning efficiency, allowing for faster and more accurate convergence.


<img src="/side_projects_diffusion/DL_diffusion_course/imgs/epoches.png" alt="epoches" width="400">
### Conclusion

This training method enables the neural network to develop a refined ability to predict noise in images, making it an effective tool for applications that require noise reduction or identification.


___
___
___

# Chapter 3: Controlling Models Through Embeddings


## How Does Embedding Become Context for the Model?
Embedding is integrated into the neural network (NN) to predict the noise added to the object you want to control. The model computes the loss and iteratively learns from the embedding. This process allows the model to use the embedding as context.

## Embedding Description
Each embedding is associated with a description or caption. During sampling time (DDPM method), you can mix these captions to create new, combined generations. For example:
- Caption 1: "Abacaxi" (Pineapple)
- Caption 2: "Cadeira" (Chair)
- Mixed Caption: "Abacaxi de Cadeira" (Pineapple Chair)

## Visual Representation

### Controlling Architecture:

<img src="/side_projects_diffusion/DL_diffusion_course/imgs/controlling_architecture.png" alt="Controlling Architecture" width="500">

## What is Context?
- Context is a vector used to control generations.

## Embedding Dimensions
Embeddings can be embedded in various dimensions. Below are visual representations:

### Context Embedding:

<img src="/side_projects_diffusion/DL_diffusion_course/imgs/context.png" alt="Context Embedding" width="500">

### Mixing Context:

<img src="../imgs/mixing_context.png" alt="Mixing Context" width="500">



___
___
___


# Chapter 4: Reasons for Slow Sampling Process

- **Too Many Steps:** The sampling process involves a large number of steps, which increases the time required.
- **Dependency on Previous Steps:** Each timestep depends on the previous one, making the process sequential and slower.

## Diffusion Models Overview

Diffusion models are a class of generative models that iteratively denoise data starting from random noise, producing high-quality samples. There are different types of diffusion models, such as DDPM and DDIM, each with its strengths and weaknesses.

### DDPM (Denoising Diffusion Probabilistic Model)

DDPM is a widely-used diffusion model that excels in generating high-quality images but often requires a large number of steps to achieve good results.

- **Advantages:**
  - High-quality image generation.
  - Well-established and extensively studied.

- **Disadvantages:**
  - Slow sampling process due to a high number of steps.
  - Each step depends on the previous one, leading to inefficiencies.

### DDIM (Denoise Diffusion Implicit Model)

DDIM is an improved version of diffusion models that addresses some of the inefficiencies found in DDPM. It modifies the denoising process to allow for fewer steps while maintaining quality.

- **Advantages:**
  - Faster sampling with fewer steps.
  - Works effectively with under 500 steps.
  - Maintains high-quality results comparable to DDPM in fewer iterations.

- **Disadvantages:**
  - May not match the quality of DDPM for very high step counts (over 500 steps).

## Comparison: DDPM vs. DDIM

| Feature                | DDPM                                | DDIM                                |
|------------------------|-------------------------------------|-------------------------------------|
| **Steps Required**     | Over 500 for high quality           | Under 500 for similar quality       |
| **Sampling Speed**     | Slower due to high step count       | Faster due to reduced steps         |
| **Dependency**         | Each step depends on the previous one | Modified process reduces dependency |
| **Use Case**           | Best for applications where high quality is paramount and speed is less critical | Ideal for scenarios where faster generation is necessary without significant loss in quality |


<img src="../imgs/ddim_flow.png" alt="DDIM flow" width="500">
DDIM modifies the traditional diffusion process, allowing for more efficient sampling. The image above shows the flow of DDIM, illustrating how it reduces the number of steps required.

## Conclusion

While DDPM is suitable for applications requiring the highest quality and can tolerate slower generation speeds, DDIM provides a faster alternative with comparable quality for under 500 steps. This makes DDIM a preferred choice for applications needing quicker turnaround times.
