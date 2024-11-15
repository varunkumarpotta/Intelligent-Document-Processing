import logging
import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from models.custom_dataset import CustomDataset

logger = logging.getLogger(__name__)

class TrainingService:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    def train_model(self, data):
        df = pd.DataFrame(data)
        
        # Ensure there is enough data for train-test split
        if len(df) < 2:
            logger.error("Not enough data to perform train-test split. At least 2 samples are required.")
            raise ValueError("Not enough data to perform train-test split. At least 2 samples are required.")

        train_texts, val_texts, train_labels, val_labels = train_test_split(df['text'], df['label'], test_size=0.1)

        train_dataset = CustomDataset(
            texts=train_texts.to_list(),
            labels=train_labels.to_list(),
            tokenizer=self.tokenizer,
            max_len=128
        )

        val_dataset = CustomDataset(
            texts=val_texts.to_list(),
            labels=val_labels.to_list(),
            tokenizer=self.tokenizer,
            max_len=128
        )

        # Set device to MPS if available, otherwise CPU
        device = torch.device('mps') if torch.backends.mps.is_available() else torch.device('cpu')
        logger.info(f"Using device: {device}")

        model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=4)
        model.to(device)

        training_args = TrainingArguments(
            output_dir='./results',
            num_train_epochs=3,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir='./logs',
            logging_steps=10,
            eval_strategy="steps",  # Evaluate every logging step
            eval_steps=10,
            save_steps=10,
            save_total_limit=2,
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset
        )

        logger.info("Starting model training")

        # Debugging: Check if inputs are properly moved to device
        def debug_data_loader(data_loader, name):
            for batch in data_loader:
                for key in batch.keys():
                    batch[key] = batch[key].to(device)
                logger.debug(f"{name} batch moved to {device}")
                break  # Check only the first batch

        # Add this to your training and validation dataset loaders if possible
        debug_data_loader(trainer.get_train_dataloader(), "Train")
        debug_data_loader(trainer.get_eval_dataloader(), "Validation")

        trainer.train()

        model.save_pretrained('./model')
        self.tokenizer.save_pretrained('./model')

        logger.info("Model trained successfully")
        return "Model trained successfully!"