from enum import Enum


class CMEKKeyTypeEnumeratesTypesOfCustomerManagedKeys(str, Enum):
    AWS_KMS = "AWS_KMS"
    GCP_CLOUD_KMS = "GCP_CLOUD_KMS"

    def __str__(self) -> str:
        return str(self.value)
