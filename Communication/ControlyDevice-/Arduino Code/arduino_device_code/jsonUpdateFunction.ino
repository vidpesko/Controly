// This function will be specific for every device
// It should use global variable "jsonDoc", which is json object
void jsonUpdate(){
  animation = jsonDoc["animation"].as<String>();
  state = jsonDoc["state"];
  activeColor = jsonDoc["active_color"].as<String>();
  restColor = jsonDoc["rest_color"].as<String>();
  activeColor = jsonDoc["active_color"].as<String>();
}