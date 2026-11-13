# Architecture indépendante

Voxcalibur est dérivé de Transcrinator 1.3.17 et utilise son moteur local Parakeet Ultra (GGUF Q8), Silero VAD et les runtimes CPU/Vulkan/CUDA. Le moteur tourne dans un processus de travail local ; la suite Ergonatus n'est pas utilisée.

Les variables de configuration sont VOXCALIBUR_DATA et VOXCALIBUR_BUNDLE. Les modèles sont vérifiés par SHA-256 avant empaquetage. Les symboles natifs transcrinator_context_set et transcrinator_transcribe_guided gardent leur nom ABI d'origine, afin de charger le runtime de guidage validé sans recompiler ni modifier les modèles.

Les dossiers models et runtimes ainsi que bundle.json accompagnent Voxcalibur.exe. Les archives complètes sont autonomes, hors ligne, et ne nécessitent pas Python installé.
