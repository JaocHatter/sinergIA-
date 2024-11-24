from pydantic import BaseModel
from typing import List, Dict, Optional

class RefinementRequest(BaseModel):
    topic: str

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "quantum computing applications in cryptography"
            }
        }

class SearchRequest(BaseModel):
    queries: List[str]
    max_results: int = 1
    sort_by: str = "Relevance"

    class Config:
        json_schema_extra = {
            "example": {
                "max_results": 3,
                "queries": [
                    "Quantum Cryptography and the Security of Quantum Key Distribution",
                    "Cryptanalysis of Some Cryptosystems Based on the Quantum Computer",
                    "Development of quantum-resistant cryptographic primitives for post-quantum era"
                    ],
                "sort_by": "Relevance"
                }
        }

class SugerenceRequest(BaseModel):
    papers: List[Dict]

    class Config:
        json_schema_extra = {
            "example": {
                "papers": [
                    {
                        "title": "Vision Transformers in 2022: An Update on Tiny ImageNet",
                        "authors": [
                        "Ethan Huynh"
                        ],
                        "abstract": "The recent advances in image transformers have shown impressive results and\nhave largely closed the gap between traditional CNN architectures. The standard\nprocedure is to train on large datasets like ImageNet-21k and then finetune on\nImageNet-1k. After finetuning, researches will often consider the transfer\nlearning performance on smaller datasets such as CIFAR-10/100 but have left out\nTiny ImageNet. This paper offers an update on vision transformers' performance\non Tiny ImageNet. I include Vision Transformer (ViT) , Data Efficient Image\nTransformer (DeiT), Class Attention in Image Transformer (CaiT), and Swin\nTransformers. In addition, Swin Transformers beats the current state-of-the-art\nresult with a validation accuracy of 91.35%. Code is available here:\nhttps://github.com/ehuynh1106/TinyImageNet-Transformers",
                        "published": "2022-05-21",
                        "updated": "2022-05-21",
                        "pdf_url": "http://arxiv.org/pdf/2205.10660v1",
                        "entry_id": "http://arxiv.org/abs/2205.10660v1",
                        "categories": "cs.CV"
                    },
                    {
                        "title": "A survey of the Vision Transformers and their CNN-Transformer based Variants",
                        "authors": [
                        "Asifullah Khan",
                        "Zunaira Rauf",
                        "Anabia Sohail",
                        "Abdul Rehman",
                        "Hifsa Asif",
                        "Aqsa Asif",
                        "Umair Farooq"
                        ],
                        "abstract": "Vision transformers have become popular as a possible substitute to\nconvolutional neural networks (CNNs) for a variety of computer vision\napplications. These transformers, with their ability to focus on global\nrelationships in images, offer large learning capacity. However, they may\nsuffer from limited generalization as they do not tend to model local\ncorrelation in images. Recently, in vision transformers hybridization of both\nthe convolution operation and self-attention mechanism has emerged, to exploit\nboth the local and global image representations. These hybrid vision\ntransformers, also referred to as CNN-Transformer architectures, have\ndemonstrated remarkable results in vision applications. Given the rapidly\ngrowing number of hybrid vision transformers, it has become necessary to\nprovide a taxonomy and explanation of these hybrid architectures. This survey\npresents a taxonomy of the recent vision transformer architectures and more\nspecifically that of the hybrid vision transformers. Additionally, the key\nfeatures of these architectures such as the attention mechanisms, positional\nembeddings, multi-scale processing, and convolution are also discussed. In\ncontrast to the previous survey papers that are primarily focused on individual\nvision transformer architectures or CNNs, this survey uniquely emphasizes the\nemerging trend of hybrid vision transformers. By showcasing the potential of\nhybrid vision transformers to deliver exceptional performance across a range of\ncomputer vision tasks, this survey sheds light on the future directions of this\nrapidly evolving architecture.",
                        "published": "2023-05-17",
                        "updated": "2024-07-27",
                        "pdf_url": "http://arxiv.org/pdf/2305.09880v4",
                        "entry_id": "http://arxiv.org/abs/2305.09880v4",
                        "categories": "cs.CV"
                    }
                    ]
            }
        }

class ConstructionRequest(BaseModel):
    papers: List[Dict]

    class Config:
        json_schema_extra = {
            "example": {
                "papers": [
                    
                ]
            }
        }

class QueryGraphRequest(BaseModel):
    topic: str

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "quantum computing cryptography applications"
            }
        }

class ErrorResponse(BaseModel):
    error: str

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Failed to process the request due to invalid input"
            }
        }

class SuccessResponse(BaseModel):
    data: Dict
    message: str = "Operation completed successfully"

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "results": ["Paper 1", "Paper 2"],
                    "metadata": {"total_count": 2}
                },
                "message": "Operation completed successfully"
            }
        }
