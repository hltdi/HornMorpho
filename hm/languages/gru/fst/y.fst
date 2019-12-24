-> start

start -> start [y;V;=;/;_]
end -> end     [X;V;=;/;_]

start -> C     [X-y]
C -> C         [X-y]
C -> start     [V;=;_;/]
C -> Cy.C      [i:y]
Cy.C -> Cy.C   [=]
Cy.C -> end    [X]

start ->
end ->
C ->