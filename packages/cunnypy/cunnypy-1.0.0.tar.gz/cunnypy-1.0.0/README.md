<h1 align="center">🦀 Cunny.py 🦀</h1>

<h3 align="center">A python library for several image boards</h3>

<p align="center">
    <a href="https://liberapay.com/GlitchyChan/donate">
        <img src="https://img.shields.io/badge/Liberapay-F6C915?style=for-the-badge&logo=liberapay&logoColor=black" alt="liberapay" />
    </a>
    <a href="https://discord.gg/ZxbYHEh">
        <img src="https://img.shields.io/badge/Discord-5865F2?logo=discord&logoColor=fff&style=for-the-badge" alt="Discord" />
    </a>
    <a href="https://twitter.com/glitchychan">
        <img src="https://img.shields.io/badge/twitter-%2300acee?&style=for-the-badge&logo=twitter&logoColor=white" alt="twitter" />
    </a>
</p>

---

<p align="center">
    <a href="#about">About</a> •
    <a href="#features">Features</a> •
    <a href="#usage">Development</a>
</p>

## **About**
This library is to make it much easier to interact with image boards with python.

## **Features**
- 🔁 Fully Async
- 🔥 Blazingly Fast™️
- 💯 Supports many sites with aliases (see [sites.json](./cunnypy/sites.json))
- 🎱 Supports random search
- ⚙️ 1 simple import to get going

## **Usage**
To get started with cunny.py simply import the library and use the search function

Example search with gelbooru
```python
import cunnypy

posts = await cunnypy.search("gel", tags=["megumin"])
print(posts)
```
This will print out a list of [Post](./cunnypy/classes.py#L30-L80) classes which you can then manipulate


Other examples can be found in the [Examples](./examples) folder
