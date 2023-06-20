// This function will be specific for every device
// It should use global variable "jsonDoc", which is json object
void jsonUpdate(){
  activeColor = jsonDoc["active_color"].as<String>();
  restColor = jsonDoc["rest_color"].as<String>();
  animation = jsonDoc["animation"].as<String>();
  state = jsonDoc["state"];
}