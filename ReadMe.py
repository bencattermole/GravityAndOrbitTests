

'''
Gravity and Orbit Tests

This is a program to demonstrate how the einstein delay and shapiro delay occur in a strong field regime binary where
there is a neutron star that presents as a pulsar (the companion is a heavy mass object: black hole, neutron star, WD)

The code in the mainloop is built from my own custom 'new project starter' if it looks like it doesnt have a purpose and
isn't called something astrophysics-y it is probably just unused code from the initial creation that I am keeping for
posterity

I have not added
 -orbital decay
 -precession of periapsis

I could add these two but it would require adding a 'system gravitational energy' value and lead to stability, there was
that video that I watched that I could use as a guide if I do intend to

 -geodetic precession

this is the hardest PK parameter to add in 2D as it is not really a 2D effect, it is the wobble in a spinning top due to
the kick given to it by the initial spin (inception esque :) ).
maybe i could add it as a slight variation of the angle that the beam is emitted over time, this would convert it to a
2D effect but I don't know if it could technically still be considered the 'same effect'
    -potentially i could just add it and not show it visually but that's a little lame

########################################################################
Unused code that code be useful in the future

not used stuff

movers have rotation value that increases over time
we don't have to draw a line to a point just a continous one in the direction of the normal of the vector that is
rotating with the mover?
need to check distance to orbital companion from the line

x, y = pygame.mouse.get_pos()

    direction_to_accel = Vector.Vector((x - mover.pos.x), (y - mover.pos.y))
    direction_to_accel.normalise_this()
    direction_to_accel.multi(scroll)

    direction_to_accel2 = Vector.Vector((x - mover2.pos.x), (y - mover2.pos.y))
    direction_to_accel2.normalise_this()
    direction_to_accel2.multi(scroll)

    mover.update_accel(direction_to_accel)
    mover2.update_accel(direction_to_accel2)


path = str(os.path.dirname(__file__))

player_IMG = pygame.image.load(f'{path}/Sprites/Tile_Selector.png').convert()
player_IMG.set_colorkey((0, 0, 0, 0))
Use the upper-left pixel color as transparent

'''