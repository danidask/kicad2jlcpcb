<!--
*** Template from https://github.com/othneildrew/Best-README-Template
*** markdown refecence https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


<br />
<p align="center">
  <h3 align="center">kicad2jlcpcb</h3>
  <p align="center">
    Plugin for KiCad 5 that allows generate files for jlcpcb pcb manufacturing and assembly service
    <br />
    <a href="https://github.com/danidask/kicad2jlcpcb"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/danidask/kicad2jlcpcb/issues">Report Bug</a>
    ·
    <a href="https://github.com/danidask/kicad2jlcpcb/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

- [Table of Contents](#table-of-contents)
- [About The Project](#about-the-project)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation or upgrade](#installation-or-upgrade)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

Plugin for KiCad 5 that allows generate files for jlcpcb pcb manufacturing and assembly service


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.


### Prerequisites

kicad2jlcpcb is a python script, you in order to install it you'll need:
* python version 3.5 or above
* pip

TODO instructions of how to install these in each operating system

### Installation or upgrade

```sh
pip install git+https://github.com/danidask/kicad2jlcpcb --upgrade
```
<em>NOTE: If you have multiple versions of python in your machine, use a specific pip version, like pip3 or pip3.6</em>


<!-- USAGE EXAMPLES -->
## Usage

schema > tools > generate bill of materials
<img src="images/screenshot_01.png" alt="screenshot">

write this in "command line" field, and then "generate"
```sh
kicad2jlcpcb %I
```
<img src="images/screenshot_02.png" alt="screenshot">



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [CPL rotation correction based of the work of Matthew Lai](https://github.com/matthewlai/JLCKicadTools)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/danidask/repo.svg?style=flat-square
[contributors-url]: https://github.com/danidask/repo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/danidask/repo.svg?style=flat-square
[forks-url]: https://github.com/danidask/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/danidask/repo.svg?style=flat-square
[stars-url]: https://github.com/danidask/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/danidask/repo.svg?style=flat-square
[issues-url]: https://github.com/danidask/repo/issues
[license-shield]: https://img.shields.io/github/license/danidask/repo.svg?style=flat-square
[license-url]: https://github.com/danidask/repo/blob/master/LICENSE.txt
