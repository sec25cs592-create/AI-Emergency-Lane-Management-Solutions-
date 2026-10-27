# Hardware Integration (Optional)

This project is designed to run on a standard Windows PC without any physical hardware. The ESP32 example below is a safe, optional demonstration for local lab experiments only.

## Important Safety Notice

- Do not connect simulated traffic-light commands to live public traffic infrastructure.
- Use dedicated test hardware or a local development board only.
- Keep any hardware integration isolated from public roads and government systems.
- This is an academic prototype and does not authorize real-world traffic control.

## ESP32 Example

The file `esp32_example.ino` contains a simple example that listens for local JSON commands over Wi-Fi or serial and updates an LED display or external indicator. The main application does not require this file to run.

## Example local interface

- Use a local network test endpoint or serial test messages.
- Always validate payloads before sending them to any hardware output.
- Keep both the Python app and the microcontroller in a controlled environment.
