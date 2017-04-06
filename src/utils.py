import os
import zipfile
import constants
import wget
from sklearn.metrics import accuracy_score, f1_score, recall_score, \
    precision_score
import configparser


def calc_metric(y_trues, y_preds):
    """
    Calculates accuracy, macro preicision, recall and f1 scores
    :param y_true: Batch of true labels
    :param y_pred: Batch of predicted labels
    :return:
    """
    assert len(y_trues) == len(y_preds)

    acc, prec, rec, f1, dim = 0, 0, 0, 0, y_trues.shape[0]
    for y_true, y_pred in zip(y_trues, y_preds):
        acc += accuracy_score(y_true, y_pred)
        prec += precision_score(y_true, y_pred, average="macro")
        rec += recall_score(y_true, y_pred, average="macro")
        f1 += f1_score(y_true, y_pred, average="macro")

    return acc / dim, prec / dim, rec / dim, f1 / dim


def read_config(config_file):
    """
    Reads the configuration file and creates a dictionary
    :param config_file: Ini file path
    :return:
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    conf_dict = dict()

    conf_dict['lr'] = float(config["MODEL"]['learning rate'])
    conf_dict['optimizer'] = config["MODEL"]['optimizer']
    conf_dict['timestep'] = int(config["MODEL"]['timestep'])
    conf_dict['word_vector_dim'] = int(
        config["MODEL"]['word embedding dimension'])
    conf_dict['char_embeddings_dim'] = int(
        config["MODEL"]['character embeddings dimension'])
    conf_dict['max_word_size'] = int(config["MODEL"]['max word length'])
    conf_dict['filter_dim'] = int(config["MODEL"]['cnn filter dimension'])
    conf_dict['lstm_hidden'] = int(config["MODEL"]['lstm hidden state dim'])
    conf_dict['batch_size'] = int(config["MODEL"]['batch size'])
    conf_dict['domain'] = config["GENERAL"]['domain']
    conf_dict['train_epochs'] = int(config["GENERAL"]['training epochs'])

    return conf_dict


def dir_creator(dirs_list):
    """
    Creates directories if they don't exist.
    :param dirs_list: List of absolute directory paths
    :return:
    """
    for d in dirs_list:
        if not os.path.exists(d):
            os.makedirs(d)
            print("Created directory", d)


def extract_zip(file, ext_dir):
    """
    Extracts the zip file to a chosen directroy
    :param file: Zip file path
    :param ext_dir: Extraction directory
    :return:
    """
    print("Extracting", file, "to", ext_dir)
    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(ext_dir)
    print("Extraction finished!\n")


def download_data(download_dir="/tmp"):
    """
    Downloads the dataset and resources required for the project.
    NOTE: You should have at least 5GB of disk space available.
    :return:
    """
    glove_dir = os.path.join(constants.RSC, "glove")
    tf_weights = os.path.join(constants.RSC, "tf_weights")

    dir_creator(
        [constants.DATA, constants.RSC, glove_dir, tf_weights])

    # Twitter glove vectors
    glove_name = os.path.join(download_dir, "glove.zip")
    if not os.path.exists(glove_name):
        print("Downloading Twitter Glove vector from", constants.GLOVE_TWITTER)
        print("This may take a while because the file size is 1.4GB")
        wget.download(constants.GLOVE_TWITTER, glove_name)
        print("Downloaded to", glove_name, "\n")
    extract_zip(glove_name, glove_dir)

    # Dataset
    print("Downloading dataset")
    for link, file in zip([constants.TRAIN, constants.VALIDATION,
                           constants.VALIDATION_NO_LABELS],
                          ["train", "valid", "eval"]):
        file = os.path.join(download_dir, file)
        if not os.path.exists(file):
            print("Downloading", link)
            wget.download(link, file)

        extract_zip(file, constants.DATA)

        # TODO Add trained weights download
