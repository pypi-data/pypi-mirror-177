from loko_client.business.base_client import PredictorClient

pclient = PredictorClient()

def test():
    import sys
    sys.path.append('/home/cecilia/loko/projects/loko_explainability/venv/lib/python3.10/site-packages/')

    from sklearn import datasets
    import pandas as pd


    pclient = PredictorClient()
    all_predictors = pclient.predictors.all()

    ### create model ###
    all_models = pclient.models.all()
    model = 'sgd_classifier_proba'
    if model in all_models:
        pclient.models.delete(model)
    pclient.models.save(model, {'__klass__': 'sk.SGDClassifier', 'loss': 'log'})

    datasets_mapping = dict(boston=dict(data=datasets.load_boston(), task='regression'),
                            diabetes=dict(data=datasets.load_diabetes(), task='regression'),
                            breast_cancer=dict(data=datasets.load_breast_cancer(), task='classification'),
                            iris=dict(data=datasets.load_iris(), task='classification'))

    for dataset, info in datasets_mapping.items():
        if dataset in all_predictors:
            print(f'PREDICTOR {dataset} ALREADY EXIST!')
            print(pclient.predictors.delete(dataset))
        ### create predictor ###
        if info['task']=='classification':
            pclient.predictors.save(dataset, model_id='sgd_classifier_proba')
        else:
            pclient.predictors.save(dataset, model_id='sgd_regressor')
        ### fit predictor ###
        X = pd.DataFrame(info['data']['data'], columns=info['data']['feature_names']).to_dict(orient='records')
        y = info['data']['target'].tolist()
        pclient.predictors.fit(dataset, data=dict(data=X, target=y), wait=True)
        info = pclient.predictors.info(dataset)
        print(info)
        if info['task']=='classification':
            print(pclient.predictors.predict(dataset, data=X, include_probs=True))
        else:
            print(pclient.predictors.predict(dataset, data=X))
        print(pclient.predictors.evaluate(dataset, data=dict(data=X, target=y)))

def test2():
    all_predictors = pclient.predictors.all()
    print('ALL PREDICTORS:', all_predictors)
    for p in all_predictors:
        print(p, pclient.predictors.info(p))
    print()
    all_models = pclient.models.all()
    print('ALL MODELS:', all_models)
    for m in all_models:
        bp = pclient.models.info(m)
        print(m, bp)
        print(pclient.models.delete(m))
        print(pclient.models.save(m, bp))
    print()
    all_transformers = pclient.transformers.all()
    print('ALL TRANSFORMERS:', all_transformers)
    for t in all_transformers:
        bp = pclient.transformers.info(t)
        print(t, bp)
        print(pclient.transformers.delete(t))
        print(pclient.transformers.save(t, bp))

    ###########################################
    print(pclient.predictors.delete('iris_copy'))
    print(pclient.predictors.copy('iris'))
    with open('/home/cecilia/Documenti/Progetti/prove-predictor/iris.zip', 'wb') as f:
        f.write(pclient.predictors.download('iris'))
    print(pclient.predictors.delete('iris'))
    with open('/home/cecilia/Documenti/Progetti/prove-predictor/iris.zip', 'rb') as f:
        print(pclient.predictors.upload(f))

    # print(pclient.predictors.release('iris'))
    print(pclient.predictors.history('iris'))
    print()
    ###########################################
    all_jobs = pclient.jobs.all()
    all_jobs = all_jobs['alive']+all_jobs['not_alive']
    print('ALL JOBS:', all_jobs)
    for j in all_jobs:
        print(j, pclient.jobs.info(j))
        print(pclient.jobs.delete(j))
    print()
    print(pclient.predictors.predict('prima_prova', data=[dict(text='hello')]))
    print()
    all_containers = pclient.containers.all()
    print('ALL CONTAINERS:', all_containers)
    for c in all_containers:
        print(pclient.containers.info(c))
        print(pclient.containers.delete(c))
    print(pclient.containers.all())

test2()