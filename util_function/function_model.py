import tensorflow as tf
from tensorflow.keras.layers import Input, Conv1D, MaxPooling1D, Flatten,LSTM, Dense, Dropout, Bidirectional,concatenate
from tensorflow.keras.models import Model,load_model
from tensorflow.keras import regularizers

def rmse(y_true, y_pred):
    return tf.sqrt(tf.reduce_mean(tf.square(y_true - y_pred)))

def rmse_percentage(y_true, y_pred):
    epsilon = 1e-10  # Small constant to avoid division by zero
    #return 100 * tf.reduce_mean(tf.abs((y_true - y_pred) / (y_true + epsilon)))
    return 100 * tf.sqrt(tf.reduce_mean(tf.square((y_true - y_pred) / y_true+ epsilon)))

def CNN_Model(input_shape, l2_factor=0.0001):
    # Define the input layer with the shape of the input data
    inputs = Input(shape=input_shape)

    # Add the first Convolutional Layer with L2 regularization
    conv1 = Conv1D(filters=64, kernel_size=2, activation='relu', padding='same',
                   kernel_regularizer=regularizers.l2(l2_factor))(inputs)
    max_pool1 = MaxPooling1D(pool_size=2)(conv1)

    # Add the second Convolutional Layer with L2 regularization
    conv2 = Conv1D(filters=128, kernel_size=2, activation='relu', padding='same',
                   kernel_regularizer=regularizers.l2(l2_factor))(max_pool1)
    max_pool2 = MaxPooling1D(pool_size=2)(conv2)

    # Flatten the output to make it 1D
    flattened = Flatten()(max_pool2)

    # Add a Dense Layer with a single neuron and a linear activation function for regression output
    output = Dense(1, activation='linear', kernel_regularizer=regularizers.l2(l2_factor))(flattened)

    # Create and compile the model
    model = Model(inputs=inputs, outputs=output)
    model.compile(optimizer='adam', loss=rmse, metrics=[rmse_percentage])

    return model

def Bilstm_Model(input_shape, l2_factor=0.0001):
    inputs = Input(shape=input_shape)
    # LSTM branch
    inputs_lstm = Input(shape=input_shape)
    bi_lstm1 = Bidirectional(LSTM(20, return_sequences=True,
                              kernel_regularizer=regularizers.l2(l2_factor)))(inputs_lstm)
    bi_lstm2 = Bidirectional(LSTM(10, return_sequences=False,
                              kernel_regularizer=regularizers.l2(l2_factor)))(bi_lstm1)


    # Dense branch
    output = Dense(1, activation='linear')(bi_lstm2)

    # Create the model
    model = Model(inputs=inputs_lstm, outputs=output)
    model.compile(optimizer='adam', loss=rmse, metrics=[rmse_percentage])

    return model


def CNN_Bilstm_sequential_Model(input_shape, l2_factor=0.0001):
    # Input layer
    inputs = Input(shape=input_shape)

    # CNN layers
    conv1 = Conv1D(filters=64, kernel_size=2, activation='relu', padding='same',
               kernel_regularizer=regularizers.l2(l2_factor))(inputs)
    maxpool1 = MaxPooling1D(pool_size=2)(conv1)
    dropout_cnn = Dropout(0.5)(maxpool1)

    # LSTM layer directly following CNN layers
    # No need to flatten the output before passing it to LSTM layers, as LSTM expects sequential input
    bi_lstm = Bidirectional(LSTM(20, return_sequences=True))(dropout_cnn)
    bi_lstm2 = Bidirectional(LSTM(10, dropout=0.03, recurrent_dropout=0.03,return_sequences=False))(bi_lstm)

    # Fully connected layers
    dense1 = Dense(25, activation='relu', kernel_regularizer=regularizers.l2(l2_factor))(bi_lstm2)
    dropout_dense = Dropout(0.5)(dense1)
    output = Dense(1, activation='linear')(dropout_dense)

    # Create the model
    model = Model(inputs=inputs, outputs=output)

    # Compile the model
    model.compile(optimizer='adam', loss=rmse, metrics=[rmse_percentage])
    return model   


def CNN_Bilstm_parallel_Model(input_shape, l2_factor=0.0001):
    # Input layer
    inputs = Input(shape=input_shape)
    # CNN branch
    inputs_cnn = Input(shape=input_shape)
    conv1 = Conv1D(filters=64, kernel_size=2, activation='relu', padding='same',kernel_regularizer=regularizers.l2(l2_factor))(inputs_cnn)
    maxpool1 = MaxPooling1D(pool_size=2)(conv1)
    conv2 = Conv1D(filters=128, kernel_size=2, activation='relu', padding='same',kernel_regularizer=regularizers.l2(l2_factor))(maxpool1)
    maxpool2 = MaxPooling1D(pool_size=2)(conv2)
    dropout_cnn = Dropout(0.5)(maxpool2)
    flatten_cnn = Flatten()(dropout_cnn)


    # Fully connected layers
    dense1 = Dense(100, activation='relu', kernel_regularizer=regularizers.l2(l2_factor))(flatten_cnn)
    dropout_dense = Dropout(0.5)(dense1)
    dense2 = Dense(50, activation='relu', kernel_regularizer=regularizers.l2(l2_factor))(dropout_dense)

    # LSTM branch
    inputs_lstm = Input(shape=input_shape)
    bi_lstm1 = Bidirectional(LSTM(20, return_sequences=True, dropout=0.03, recurrent_dropout=0.03))(inputs_lstm)
    bi_lstm2 = Bidirectional(LSTM(10, return_sequences=True, dropout=0.03, recurrent_dropout=0.03))(bi_lstm1)
    flatten_lstm = Flatten()(bi_lstm2)
    #Combine the outputs of the two branches
    combined = concatenate([dense2, flatten_lstm])
    # Final dense layer for prediction
    output = Dense(1, activation='linear')(combined)

    # Create the model
    model = Model(inputs=[inputs_cnn, inputs_lstm], outputs=output)
    # Compile the model
    model.compile(optimizer='adam', loss=rmse, metrics=[rmse_percentage])
    return model


def Autoencoder_Model(input_dim, timesteps, latent_dim=50, l2_factor=0.0001):
    # Define the encoder with L2 regularization
    inputs = Input(shape=(timesteps, input_dim))
    encoded = LSTM(latent_dim, return_sequences=True, 
                                 kernel_regularizer=regularizers.l2(l2_factor))(inputs)

    # Define the decoder, also with L2 regularization
    # Ensure the output dimension matches the input dimension of the autoencoder
    decoded = LSTM(input_dim, return_sequences=True, 
                                 kernel_regularizer=regularizers.l2(l2_factor))(encoded)

    # Define the autoencoder model
    autoencoder = Model(inputs= inputs, outputs =decoded)
    # Assuming rmse and rmse_percentage are already defined elsewhere
    autoencoder.compile(optimizer='adam', loss=rmse, metrics=[rmse_percentage])
    
    return autoencoder



def Auto_Bilstm_model(encoder_path, bilstm_autoencoder_path, custom_objects=None):
    if custom_objects is None:
        custom_objects = {'rmse': rmse, 'rmse_percentage': rmse_percentage}
    # Load the pre-trained encoder and Autoencoder_BiLSTM models
    encoder_model = load_model(encoder_path, custom_objects=custom_objects)
    autoencoder_bilstm_model = load_model(bilstm_autoencoder_path, custom_objects=custom_objects)

    # Connect the encoder output to the Autoencoder_BiLSTM model
    encoded_output = encoder_model.output
    bilstm_output = autoencoder_bilstm_model(encoded_output)

    # Create the new fine-tuned model
    fine_tuned_model = Model(inputs=encoder_model.input, outputs=bilstm_output)

    # Freeze all layers except the last one
    for layer in fine_tuned_model.layers[:-1]:
        layer.trainable = False
    fine_tuned_model.layers[-1].trainable = True

    return fine_tuned_model