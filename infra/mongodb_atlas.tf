terraform {
  required_providers {
    mongodbatlas = {
      source  = "mongodb/mongodbatlas"
      version = "~> 1.14.0"
    }
  }
}

# Terraform MongoDB Atlas IaC
# Requiere: exportar variables de entorno ATLAS_PUBLIC_KEY y ATLAS_PRIVATE_KEY
# Docs: https://registry.terraform.io/providers/mongodb/mongodb/latest/docs

provider "mongodbatlas" {
  public_key  = var.atlas_public_key
  private_key = var.atlas_private_key
}

variable "atlas_public_key" {}
variable "atlas_private_key" {}
variable "project_name" { default = "UNI-Postulantes" }
variable "org_id" {} # Debes obtener tu Organization ID de Atlas
variable "db_user_password" {} # Contraseña segura para el usuario no admin

resource "mongodbatlas_project" "uni_postulantes" {
  name   = var.project_name
  org_id = var.org_id
}

resource "mongodbatlas_database_user" "uni_user" {
  username           = "uni_postulante_user"
  password           = var.db_user_password
  project_id         = mongodbatlas_project.uni_postulantes.id
  auth_database_name = "admin"
  roles {
    role_name     = "readWrite"
    database_name = "oltp_postulantes"
  }
  roles {
    role_name     = "readWrite"
    database_name = "olap_postulantes"
  }
}

# Opcional: crear IP whitelist para tu IP local
resource "mongodbatlas_project_ip_access_list" "my_ip" {
  project_id = mongodbatlas_project.uni_postulantes.id
  cidr_block = "0.0.0.0/0" # Permite acceso desde cualquier IP (ajusta para producción)
  comment    = "Acceso abierto para pruebas"
}

# NOTA: MongoDB Atlas crea las bases de datos y colecciones al primer uso.
# Puedes usar mongosh o el ETL para crear las colecciones.

# Uso:
# 1. Exporta tus claves Atlas:
#    export TF_VAR_atlas_public_key=...
#    export TF_VAR_atlas_private_key=...
#    export TF_VAR_org_id=...
#    export TF_VAR_db_user_password=...
# 2. Ejecuta:
#    terraform init
#    terraform apply 