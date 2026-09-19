function [x,X]=idprev(X,t,Y)

k=X(1);
T1=abs(X(2));
T2=abs(X(3));
Tm=abs(X(4));
H=tf(k,conv([T1 1],[T2 1]));
set(H,'InputDelay',Tm);

y=step(H,t);
x=(y-Y)'*(y-Y);

%%%%%%%%%%%%%%%%  affichage %%%%%%%%%%%%%%%%%%%

figure(5)
plot(t,y,t,Y);grid
taille=15;
decalage=t(end)/8;
Tprint=t(round(0.7*length(t)));

a=text(Tprint,0.1*X(1),'K =');set(a,'FontSize',taille)
a=text(Tprint+decalage,0.1*X(1),num2str(X(1)));set(a,'FontSize',taille)

a=text(Tprint,0.25*X(1),'T1 =');set(a,'FontSize',taille)
a=text(Tprint+decalage,0.25*X(1),num2str(abs(X(2))));set(a,'FontSize',taille)

a=text(Tprint,0.40*X(1),'T2 =');set(a,'FontSize',taille)
a=text(Tprint+decalage,0.4*X(1),num2str(abs(X(3))));set(a,'FontSize',taille)

a=text(Tprint,0.55*X(1),'Tm =');set(a,'FontSize',taille)
a=text(Tprint+decalage,0.55*X(1),num2str(abs(X(4))));set(a,'FontSize',taille)

a=text(Tprint,0.70*X(1),'J =');set(a,'FontSize',taille)
a=text(Tprint+decalage,0.70*X(1),num2str(x));set(a,'FontSize',taille)

title('Identification récursive de la dynamique de perturbation G2')
xlabel(' Fonction de coût J = somme des (Yréel - Ymodel) au carré  ')
drawnow

X(2) = abs(X(2));
X(3) = abs(X(3));
X(4) = abs(X(4));
