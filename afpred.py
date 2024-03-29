import time, os, sys
from sys import version_info
from pathlib import Path
from epitope.protein import Protein

class AFPred():
  def __init__(self):
    self.python_version = f"{version_info.major}.{version_info.minor}"
    if not os.path.isfile("COLABFOLD_READY"):
      print("installing colabfold...")
      os.system("pip install -q --no-warn-conflicts 'colabfold[alphafold-minus-jax] @ git+https://github.com/sokrypton/ColabFold'")
      os.system("ln -s /usr/local/lib/python3.*/dist-packages/colabfold colabfold")
      os.system("ln -s /usr/local/lib/python3.*/dist-packages/alphafold alphafold")
      os.system("touch COLABFOLD_READY")
    if not os.path.isfile("CONDA_READY"):
      print("installing conda...")
      os.system("wget -qnc https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh")
      os.system("bash Mambaforge-Linux-x86_64.sh -bfp /usr/local")
      os.system("mamba config --set auto_update_conda false")
      os.system("touch CONDA_READY")
    if not os.path.isfile("AMBER_READY"):
      print("installing amber...")
      os.system(f"mamba install -y -c conda-forge openmm=7.7.0 python='{self.python_version}' pdbfixer")
      os.system("touch AMBER_READY")

  def colabfold_predict(self, pdb_path, num_recycles=5):
    pdb_id = pdb_path.split('/')[-1].split('.')[0]
    from colabfold.download import download_alphafold_params, default_data_dir
    from colabfold.utils import setup_logging
    from colabfold.batch import get_queries, run, set_model_type
    assert not "1" in os.popen('nvidia-smi | grep "Tesla K80" | wc -l').read()
    # Need for pdbfixer to import
    if f"/usr/local/lib/python{self.python_version}/site-packages/" not in sys.path:
        sys.path.insert(0, f"/usr/local/lib/python{self.python_version}/site-packages/")

    p = Protein(pdb_path)
    query_sequence = ''.join(p.sequence.values())
    results_dir = pdb_path.split('.')[0]
    os.makedirs(results_dir, exist_ok=True)
    queries_path = os.path.join(results_dir, f"{pdb_id}.csv")
    with open(queries_path, "w") as text_file:
      text_file.write(f"id,sequence\n{pdb_id},{query_sequence}")

    print("pdb_id",pdb_id)
    print("sequence",query_sequence)
    print("length",len(query_sequence))

    log_filename = os.path.join(results_dir,"log.txt")
    setup_logging(Path(log_filename))
    queries, is_complex = get_queries(queries_path)
    model_type = set_model_type(is_complex, "alphafold2_ptm")
    download_alphafold_params(model_type, Path("."))

    results = run(
        queries=queries,
        result_dir=results_dir,
        use_templates=False,
        custom_template_path=None,
        num_relax=1,
        msa_mode="mmseqs2_uniref_env",
        model_type=model_type,
        num_models=1,
        num_recycles=num_recycles,
        relax_max_iterations=200,
        recycle_early_stop_tolerance=None,
        num_seeds=1,
        use_dropout=False,
        model_order=[1],
        is_complex=is_complex,
        data_dir=Path("."),
        keep_existing_results=False,
        rank_by="auto",
        pair_mode="unpaired_paired",
        pairing_strategy="greedy",
        stop_at_score=float(100),
        prediction_callback=None,
        dpi=200,
        zip_results=False,
        save_all=False,
        max_msa=None,
        use_cluster_profile=True,
        input_features_callback=None,
        save_recycles=False,
        user_agent="colabfold/google-colab-main",
    )
    return results
