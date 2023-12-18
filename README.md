
# ShipAI

## Team Members
- Hok Lai Lin - hlin153@ucr.edu - [GitHub](https://github.com/windasadf)
- Hanlin Zha - hzha001@ucr.edu - [GitHub](https://github.com/AozakiKoriko)
- Zipeng Zhu - zzhu098@ucr.edu - [GitHub](https://github.com/zzhu17)
- Sihua Lin - slin177@ucr.edu - [GitHub](https://github.com/Linsihua)

## Software Overview
Our software utilizes a variety of algorithms (A*, Dijkstra, backtracking, etc.) to handle the path planning and balance problems of loading and unloading cargo from ships. It can intelligently and efficiently compute the optimal (or near-optimal) steps and required time for loading and unloading cargo on ships up to 8x12 size. The software also addresses legal balance issues for ships of up to 8x12 size. Additional features include operation logging, checkpoint backup, and more. We offer a web-based user interface and a downloadable offline application. The web version supports various operating systems, while the downloadable version currently supports Windows only.

## Features
1. **Load and Unload Cargo**: Users input cargo to be unloaded from the ship and the names and weights of cargo to be loaded. The system automatically calculates the optimal (or near-optimal) steps and required time.
2. **Balance Cargo**: Users upload a manifest, and the system calculates the optimal (or near-optimal) steps to achieve optimal (legal) balance.
3. **Checkpoint Backup**: In case of a device power outage, the system can resume from the last step before the outage.
4. **Log Recording**: Users' various actions are recorded in `log.txt`.
5. **Output**: The system updates and outputs a new manifest.

## Installation and Usage
### Standard Flask+Python+HTML Setup
1. **Prerequisites**: 
   - Ensure Python, Flask, and necessary libraries are installed.
   - Clone the repository from GitHub.

2. **Environment Setup**:
   - Navigate to the cloned directory and set up a virtual environment.
   - Activate the virtual environment and install dependencies from `requirements.txt`.

3. **Run the Application**:
   - Start the Flask server and access the application via a web browser.

### Downloadable .exe Application
- Download the `.exe` file from the releases section.
- Run the executable to start the application.

## Contributing
Contributions to our project are welcome. Please submit pull requests or open issues for suggestions and improvements.

## License
[Specify the license here, if applicable]