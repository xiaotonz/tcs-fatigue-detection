# Configure Azure Provider
provider "azurerm" {
  features {}
  subscription_id = "b462f50d-0ab3-4f18-9bcb-f90828f74c55"
}

# Create Azure Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "tcs-fatigue-detection-group"
  location = "East US"
}

# Define Azure SQL Server
resource "azurerm_sql_server" "sql" {
  name                         = "tcs-fatigue-server"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"
  administrator_login          = "admin"
  administrator_login_password = "sql@server12345"
}

# Create Azure SQL Database
resource "azurerm_sql_database" "db" {
  name                = "tcs-fatigue-server"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  server_name         = azurerm_sql_server.sql.name
}

# Deploy Azure Kubernetes Service (AKS)
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "tcs-aks"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "tcs-aks"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_D2_v2"
  }
  identity {
    type = "SystemAssigned"  # Specifies the managed identity type
  }
}
resource "azurerm_container_registry" "acr" {
  name                     = "tcsFatigueAcr"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  sku                      = "Basic"  # Choose the desired SKU (e.g., Basic, Standard, Premium)
  

}

