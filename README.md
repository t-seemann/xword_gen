Notizen:

Generell ist es Grid-artig:

+--+--+--+--+--+--+--+--+
|  |  |  |  |  |  |  |  |
+--+--+--+--+--+--+--+--+
|  |  |  |  |xx|  |  |  |
+--+--+--+--+--+--+--+--+
|xx|xx|xx|xx|xx|xx|  |  |
+--+--+--+--+--+--+--+--+
|  |  |  |  |xx|  |  |  |
+--+--+--+--+--+--+--+--+
|  |  |  |  |xx|  |  |  |
+--+--+--+--+--+--+--+--+


Vielleicht ist der einfachste Ansatz, ein generative:

Pseudocode:
'
set_words = []

direction = "vertical"

while (queue.isNonEmpty)

  word = queue.poll()
  
  if set_words = empty_set
    set_words.add(word)
  else
    for w in set_words
      if matchesCharater(word, w)
        place(word, direction)
        check_place_possible()
        change_direction(direction)
    
    if not_placed
      queue.add(word)
 
print(crossword) 

  
'

# Algorithm:


