# The build-stage image:
    FROM continuumio/miniconda3:24.3.0-0 AS build

    # Install necessary packages
    RUN conda config --set always_yes yes --set changeps1 no
    RUN conda update --all -y
    RUN conda config --add channels conda-forge
    RUN conda install -c conda-forge conda-pack
            
    # Install libmamba and set it as default solver
    RUN conda install -n base conda-libmamba-solver
    RUN conda config --set solver libmamba
        
    # Install the package as normal:
    # the prod_environment.yaml file is downloaded from the git repo by the azure pipeline. 
    # If this fails, then the repo is specified before this build doesn't have the prod_environment.yaml at its top level
    RUN conda install -c conda-forge conda-pack
    COPY prod_environment.yaml .
    RUN conda env create -f prod_environment.yaml
    RUN conda-pack -n cs3dash -o /tmp/env.tar
    RUN conda clean --all --force-pkgs-dirs -y
    RUN mkdir /env &&\
        cd /env &&\ 
        tar xf /tmp/env.tar &&\
        rm /tmp/env.tar
        
    # We've put env in same path it'll be in final image,
    # so now fix up paths:
    RUN /env/bin/conda-unpack
    
    # The runtime-stage image; we can use Alpine as the
    # base image since the Conda env also includes Python
    # for us.
    FROM debian:buster-slim AS runtime
    
    # Copy /env from the previous stage:
    COPY --from=build /env /env
    # Install git, wget
    RUN apt-get update
    RUN apt-get -y install git wget curl
    RUN apt-get clean all
    RUN apt-get purge
    RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
    
    # Open 80 for http
    EXPOSE 80
    
    # When image is run, run the code with the environment
    # activated env and git clone repo provided as first argument to setup_run_server.sh and cd to it
    # and source run_server.sh there expecting it to start server listening to port 80
    # Use bash instead of sh
    COPY run_server.sh .
    
    ENTRYPOINT ["/bin/bash", "run_server.sh"]