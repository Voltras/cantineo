# Cantineo

Cantineo est un projet d'application mobile web qui a pour but de permettre à un gérant d'une cantine de faire passer des repas à des employés.
Il s'agit d'une application compatible avec Android uniquement.

## Compilation sur mobile
Windows/Linux:
[Télécharger Node.js](https://nodejs.org/en/download)

[Télécharger OpenJDK11/OpenJDK17](https://adoptium.net/)
La version de OpenJDK doit être entre 11 et 17.
Une fois installé, exécutez `java -version` pour vérifier la version.

[Télécharger Android Studio](https://developer.android.com/studio)
Vous avez besoin du SDK Android pour compiler l'application.
Vérifiez l'installation avec : `sdkmanager --list`

[Télécharger Gradle pour Windows](https://gradle.org/install/)
Gradle est nécessaire pour compiler les applications Android.
Pour Linux : `sudo apt install gradle`
Vérifiez l'installation avec : `gradle -v`
Pour les systèmes windows : Si la commande ne fonctionne pas, voir la section Variables d'Environnement

### Variables d'environnement
Windows :
Ouvrez `Paramètres > Système > Informations système avancées > Variables d’environnement`
Ajoutez ces chemins dans `Path` :
C:\Program Files\Java\jdk-11\bin
C:\Gradle\bin
C:\Users\VotreNomUtilisateur\AppData\Local\Android\Sdk\platform-tools
C:\Users\VotreNomUtilisateur\AppData\Local\Android\Sdk\cmdline-tools\latest\bin

Ajoutez également ces variables utilisateur :
ANDROID_HOME = `C:\Users\VotreNomUtilisateur\AppData\Local\Android\Sdk`
JAVA_HOME = `C:\Program Files\Java\jdk-17` (remplacez la version par celle que vous utilisez)

Redémarrez votre PC après ces changements.

Linux:
Ajoutez ceci dans `~/.bashrc` ou `~/.zshrc` :
```sh
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$ANDROID_HOME/platform-tools:$ANDROID_HOME/tools:$PATH
export PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$PATH
export PATH=$JAVA_HOME/bin:$PATH
export PATH=/opt/gradle/bin:$PATH
```

Rechargez le fichier :
```sh
source ~/.bashrc  # ou source ~/.zshrc
```

Testez ADB :
```sh
adb devices
```

Rendez-vous dans le dossier `gestion-cantine/www` puis remplacez les fichiers présents par le fichier `index.html` se trouvant à la racine du projet pour exécuter les commandes suivantes :
```sh
npm install -g cordova
cordova build android
```

Une fois la compilation terminée, avec un appareil mobile en mode développeur qui autorise les téléchargements en USB (Généralement dans les paramètres du mode développeur. Si vous ne savez pas mettre votre téléphone en mode développeur, référez vous à la documentation en ligne suivant votre téléphone.) Exécutez la commande suivante :
`cordova run android`

## Utilisation sur Ordinateur
Il suffit d'ouvrir le fichier 'index.html' dans votre navigateur.
