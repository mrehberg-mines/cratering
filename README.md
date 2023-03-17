# cratering
This repo allows you to make simulated craters on a surface and measure the regolith and protolith heights

It takes a little bit to run, so figures from an 800 crater simulation have been updated.

The goal was to create a basic simulation to match the regolith growth plots from Quaide and Oberbeck. There is good matching from the Regolith Mean Height plot, and the base height map shows some similarities to the Moon's surface. 
Getting a similar plot to the Moon's surface took a few trials. The main change was having to "overwrite" the current topography to match that of the incoming crater. The physical interpretation of this is that incoming meteors would create a smooth crater shape regardless of the surrounding slope of the regolith. 

Some interesting takeaways are that the regolith and the protolith height can be mapped. This could, if expanded and applied much further, provide a way to estimate how deep regolith would be at given points on the a planet's or moon's surface given crater depictions. 

There would likely have to be a lot of actual correlations to more physical properties added to practically use this simulation. 
