docker build -t odinluo/suishouji .
docker push odinluo/suishouji
docker save -o suishouji.tar odinluo/suishouji:latest
move suishouji.tar \\10.0.0.1\docker\images