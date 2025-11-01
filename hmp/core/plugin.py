import importlib.util

class PluginManager:
    def __init__(self, registry):
        self.registry = registry

    def load_plugin(self, plugin_path: str):
        print(f"[PluginManager] Tentando carregar plugin de: {plugin_path}")
        try:
            module_name = f"hmp_plugin_{plugin_path.replace('/', '_').replace('.', '_')}"
            spec = importlib.util.spec_from_file_location(module_name, plugin_path)
            if spec and spec.loader:
                plugin_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(plugin_module)
                if hasattr(plugin_module, 'register_hmp_components') and callable(plugin_module.register_hmp_components):
                    plugin_module.register_hmp_components(self.registry)
                    print(f"[PluginManager] Plugin {plugin_path} carregado e componentes registrados.")
                else:
                    print(f"[PluginManager] Plugin {plugin_path} não possui 'register_hmp_components'.")
            else:
                print(f"[PluginManager] Não foi possível criar spec para o plugin: {plugin_path}")
        except FileNotFoundError:
            print(f"[PluginManager] Arquivo do plugin não encontrado: {plugin_path}")
        except Exception as e:
            print(f"[PluginManager] Erro ao carregar plugin {plugin_path}: {e}")
