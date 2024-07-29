resource "helm_release" "kyverno" {
  name = "security"

  repository       = "https://kyverno.github.io/kyverno/"
  chart            = "kyverno"
  namespace        = "kyverno"
  create_namespace = true
  depends_on = [helm_release.prometheus]

}